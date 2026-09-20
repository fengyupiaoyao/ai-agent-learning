import os
from pathlib import Path
from dotenv import load_dotenv

import asyncio

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# 按脚本位置加载项目根目录的配置，不依赖运行目录
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

model = ChatOpenAI(
    model="qwen-plus",
    api_key=os.environ["OPENAI_API_KEY"],
    base_url="https://ws-wopagvlf3afu5baf.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        你是一个 AI Agent。

        请回答用户的问题。
        """
    ),
    (
        "human",
        "{question}"
    )
])

chain = prompt | model


async def run_agent(question: str):
    print("Agent 开始运行...\n")

    print("正在分析问题...\n")

    await asyncio.sleep(2)

    print("开始生成回答：")

    async for chunk in chain.astream({"question": question}):
        print(chunk.content, end="", flush=True)

    print("\n回答生成完毕。")

asyncio.run(run_agent("为什么 Python 的 async/await 很重要？"))
