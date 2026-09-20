import os
from pathlib import Path
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

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
        "你是一名 Python 老师，请用通俗易懂的方式回答问题。"
    ),
    (
        "human",
        "{question}"
    )
])

answer_chain = prompt | model

chain = RunnableParallel(question=RunnablePassthrough(),
                         answer=answer_chain)

result = chain.invoke({"question": "如何在 Python 中实现一个简单的计算器？"})

print("问题：")
print(result["question"])

print()

print("回答：")
print(result["answer"].content)
