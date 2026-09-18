import os
from pathlib import Path

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
            "你是一名{role}"
        ),
        (
            "human",
            "{question}"
        ),
    ]
)


chain = prompt | model

response = chain.invoke({
    "role": "AI Agent 专家",
    "question": "什么是 Tool Calling？"
})

print(response.content)
