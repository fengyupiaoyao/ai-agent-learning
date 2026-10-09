import json
from pydantic import BaseModel

from typing import TypedDict
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI

from langgraph.config import get_stream_writer

import os
from dotenv import load_dotenv
load_dotenv()


class AgentState(TypedDict):
    question: str


llm = ChatOpenAI(
    model="qwen3.8-max",
    api_key=os.environ["OPENAI_API_KEY"],
    base_url="https://ws-wopagvlf3afu5baf.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
    temperature=0,
)


# def agent_node(state: AgentState):
#     response = llm.invoke(state["question"])
#     return {}

async def agent_node(state: AgentState):
    writer = get_stream_writer()

    async for chunk in llm.astream(state["question"]):
        if chunk.content:
            writer({"content": chunk.content})

    return {}

builder = StateGraph(AgentState)

builder.add_node("agent", agent_node)
builder.add_edge(START, "agent")
builder.add_edge("agent", END)

graph = builder.compile()

app = FastAPI(title="Day 36 Streaming Agent")


class ChatRequest(BaseModel):
    question: str


def encode_sse(event: str, data: dict) -> str:
    payload = json.dumps(data, ensure_ascii=False)
    return f"event: {event}\ndata: {payload}\n\n"


@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    async def generate():
        try:
            # async for chunk in graph.astream(
            #     {"question": request.question},
            #     # stream_mode="messages"
            #     stream_mode="custom"
            # ):
            #     message_chunk, metadata = chunk
            #     if metadata.get("langgraph_node") != "agent":
            #         continue
            #     content = message_chunk.content

            #     if isinstance(content, str) and content:
            #         yield encode_sse(
            #             "token",
            #             {"content": content}
            #         )
            # yield encode_sse("done", {"status": "completed"})

            async for chunk in graph.astream(
                {"question": request.question},
                stream_mode="custom",
            ):
                yield encode_sse("token", chunk)
            yield encode_sse("done", {"status": "completed"})
        except Exception as e:
            yield encode_sse("error", {"message": str(e)})
    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no"
        },
    )


@app.get("/health")
async def health():
    return {"status": "ok"}
