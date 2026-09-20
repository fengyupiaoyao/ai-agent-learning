import os
from pathlib import Path
import asyncio

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# 按脚本位置加载项目根目录的配置，不依赖运行目录
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

model = ChatOpenAI(
    model="qwen-plus",
    api_key=os.environ["OPENAI_API_KEY"],
    base_url="https://ws-wopagvlf3afu5baf.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "你是一名 Python 老师"
        ),
        (
            "human",
            "{question}"
        ),
    ]
)

chain = prompt | model


async def main():
    question = "Python 有什么特点？"
    async for chunk in chain.astream(question):
        print(chunk.content, end="", flush=True)

asyncio.run(main())
