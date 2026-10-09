
import json
import logging
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, MessagesState
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver

import os
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DB_PATH = "checkpoints.sqlite"


# 1. 初始化模型
llm = ChatOpenAI(
    model="qwen3.8-max",
    api_key=os.environ["OPENAI_API_KEY"],
    base_url="https://ws-wopagvlf3afu5baf.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
    temperature=0,
)


# 2. 定义 Agent 节点
async def call_model(state: MessagesState):
    response = await llm.ainvoke(state["messages"])
    return {"messages": [response]}


# 3. 定义 Graph Builder
builder = StateGraph(MessagesState)
builder.add_node("assistant", call_model)
builder.add_edge(START, "assistant")


# 4. FastAPI 生命周期管理
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with AsyncSqliteSaver.from_conn_string(
        DB_PATH
    ) as checkpointer:
        # 编译时注入持久化 Checkpointer
        app.state.graph = builder.compile(
            checkpointer=checkpointer
        )
        yield


app = FastAPI(
    title="Day 38 Persistent Agent",
    lifespan=lifespan,
)


class ChatRequest(BaseModel):
    question: str = Field(min_length=1, max_length=10000)
    thread_id: str = Field(min_length=1, max_length=100)


def encode_sse(event: str, data: dict[str, Any]) -> str:
    return (
        f"event: {event}\n"
        f"data: {json.dumps(data, ensure_ascii=False)}\n\n"
    )


@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    graph = app.state.graph

    config = {
        "configurable": {
            "thread_id": request.thread_id,
        }
    }

    async def generate():
        try:
            async for chunk in graph.astream(
                {
                    "messages": [
                        {
                            "role": "user",
                            "content": request.question,
                        }
                    ]
                },
                config=config,
                stream_mode="messages",
            ):
                message_chunk, metadata = chunk

                if metadata.get("langgraph_node") != "assistant":
                    continue

                content = message_chunk.content

                if isinstance(content, str) and content:
                    yield encode_sse(
                        "token",
                        {"content": content},
                    )

            yield encode_sse(
                "done",
                {"status": "completed"},
            )

        except Exception:
            logger.exception("Agent streaming failed")
            yield encode_sse(
                "error",
                {"message": "Agent 执行失败，请稍后重试"},
            )

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/debug/threads/{thread_id}")
async def debug_threads(thread_id: str):
    graph = app.state.graph

    config = {
        "configurable": {
            "thread_id": thread_id,
        }
    }

    history = []

    async for checkpoint in graph.aget_state_history(config):
        history.append(
            {
                "checkpoint_id": checkpoint.config[
                    "configurable"
                ].get("checkpoint_id"),
                "next": list(checkpoint.next),
                "message_count": len(
                    checkpoint.values.get("message", [])
                )
            }
        )
    return {
        "thread_id": thread_id,
        "checkpoints": history,
    }
