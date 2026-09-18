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
            "你是一名{role}，回答风格为{style}"
        ),
        (
            "human",
            "{question}"
        ),
    ]
)
chain = prompt | model

# response = chain.invoke({
#     "role": "Python 老师",
#     "style": "适合初学者",
#     "question": "什么是asyncio？"
# })
# print(response.content)

# response2 = chain.invoke({
#     "role": "Python 面试官",
#     "style": "面试回答风格",
#     "question": "什么是 asyncio？"
# })

# print(response2.content)

while True:
    question = input("问题: ")
    if question == "exit":
        break

    response = chain.invoke({
        "role": "Python 老师",
        "style": "适合初学者",
        "question": question
    })
    print(response.content)
