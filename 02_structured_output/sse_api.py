from fastapi import FastAPI
from sse_starlette.sse import EventSourceResponse

import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# 按脚本位置加载项目根目录的配置，不依赖运行目录
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

model = ChatOpenAI(
    model="qwen-plus",
    api_key=os.environ["OPENAI_API_KEY"],
    base_url="https://ws-wopagvlf3afu5baf.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

app = FastAPI()


async def genarate():
    async for chunk in model.astream("请介绍一下 langchain"):
        yield {
            "event": "message",
            "data": chunk.content,
        }


@app.get("/chat")
async def chat():
    return EventSourceResponse(genarate())
