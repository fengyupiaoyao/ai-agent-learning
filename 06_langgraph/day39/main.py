import json
import logging
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.store.memory import InMemoryStore
from langgraph.runtime import Runtime

import os
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class Context:
    user_id: str


llm = ChatOpenAI(
    model="qwen3.8-max",
    api_key=os.environ["OPENAI_API_KEY"],
    base_url="https://ws-wopagvlf3afu5baf.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
    temperature=0,
)


async def call_model(
    state: MessagesState,
    runtime: Runtime[Context]
):
    user_id = runtime.context.user_id

    namespace = (user_id, "memories")

    profile = runtime.store.get(namespace, "profile")

    if profile:
        memory_text = json.dumps(
            profile.value,
            ensure_ascii=False,
        )
    else:
        memory_text = "目前没有保存的用户资料"

    system_message = SystemMessage(
        content=(
            "你是一个 AI Agent 学习助手。\n"
            "下面是当前用户主动保存的长期记忆：\n"
            f"{memory_text}\n\n"
            "回答时可以使用这些信息个性化建议。"
            "如果资料中没有答案，不要编造。"
        )
    )

    response = await llm.ainvoke([
        system_message,
        *state["messages"]
    ])

    return {"messages": [response]}

builder = StateGraph(MessagesState, context_schema=Context)
builder.add_node("call_model", call_model)
builder.add_edge(START, "call_model")
builder.add_edge("call_model", END)

store = InMemoryStore()
checkpointer = InMemorySaver()

graph = builder.compile(
    store=store,
    checkpointer=checkpointer,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(
    title=" Day 39",
    lifespan=lifespan
)


class MemoryRequest(BaseModel):
    user_id: str = Field(min_length=1, max_length=100)
    name: str = Field(min_length=1, max_length=100)
    programming_language: str = Field(
        min_length=1,
        max_length=100,
    )
    goal: str = Field(min_length=1, max_length=500)


class ChatRequest(BaseModel):
    user_id: str = Field(min_length=1, max_length=100)
    thread_id: str = Field(min_length=1, max_length=100)
    question: str = Field(min_length=1, max_length=10000)


def encode_sse(event: str, data: dict[str, Any]) -> str:
    return (
        f"event: {event}\n"
        f"data: {json.dumps(data, ensure_ascii=False)}\n\n"
    )


@app.put("/memory")
async def save_memory(request: MemoryRequest):
    namespace = (request.user_id, "memories")

    store.put(
        namespace,
        "profile",
        {
            "name": request.name,
            "programming_language": (
                request.programming_language
            ),
            "goal": request.goal,
        },
    )

    return {
        "status": "saved",
        "user_id": request.user_id,
    }


# 8. 查询长期记忆
@app.get("/memory/{user_id}")
async def get_memory(user_id: str):
    item = store.get((user_id, "memories"), "profile")

    if item is None:
        raise HTTPException(
            status_code=404,
            detail="未找到用户长期记忆",
        )

    return item.value


@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    config = {
        "configurable": {
            "thread_id": request.thread_id
        }
    }

    async def generate():
        try:
            async for chunk in graph.astream({
                "messages": [
                    {
                        "role": "user",
                        "content": request.question,
                    }
                ]
            },
                config=config,
                context=Context(user_id=request.user_id),
                stream_mode="messages",
            ):
                message_chunk, metadata = chunk

                if metadata.get("langgraph_node") != "call_model":
                    continue

                content = message_chunk.content

                if isinstance(content, str) and content:
                    yield encode_sse(
                        "token",
                        {"content": content},
                    )
                elif isinstance(content, list):
                    for item in content:
                        if isinstance(item, dict) and item.get("type") == "text" and item.get("text"):
                            yield encode_sse(
                                "token",
                                {"content": item["text"]},
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
