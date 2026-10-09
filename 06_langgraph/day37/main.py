
import json
import logging
from turtle import dot
from typing import Any

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, MessagesState
from langgraph.checkpoint.memory import InMemorySaver

import os
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Day 37 - Agent Memory + SSE")

llm = ChatOpenAI(
    model="qwen3.8-max",
    api_key=os.environ["OPENAI_API_KEY"],
    base_url="https://ws-wopagvlf3afu5baf.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
    temperature=0,
)


# 1. 定义模型节点
async def call_model(state: MessagesState):
    response = await llm.ainvoke(state["messages"])
    return {"messages": [response]}


# 2. 构建带 Checkpointer 的 LangGraph
builder = StateGraph(MessagesState)
builder.add_node("assistant", call_model)
builder.add_edge(START, "assistant")

checkpointer = InMemorySaver()
graph = builder.compile(checkpointer=checkpointer)


# 3. 请求模型
class ChatRequest(BaseModel):
    question: str = Field(min_length=1, max_length=10000)
    thread_id: str = Field(min_length=1, max_length=100)


# 4. SSE 编码
def encode_sse(event: str, data: dict[str, Any]) -> str:
    payload = json.dumps(data, ensure_ascii=False)
    return f"event: {event}\ndata: {payload}\n\n"


# 5. 多轮对话 + 流式输出
@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
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

                # 只输出 Agent 节点的消息
                if metadata.get("langgraph_node") != "assistant":
                    continue

                content = message_chunk.content

                # 忽略空内容和非文本内容
                if isinstance(content, str) and content:
                    yield encode_sse(
                        "token",
                        {"content": content},
                    )

            yield encode_sse("done", {"status": "completed"})

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
