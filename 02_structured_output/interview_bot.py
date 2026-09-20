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
        """
        你是一名资深 Python 面试官。

        请用面试准备的角度回答问题：
        1. 先给出一句话定义
        2. 再解释核心原理
        3. 最后给出一个简单例子
        """
    ),
    (
        "human",
        "{question}"
    )
])

chain = prompt | model

questions = [
    "什么是 Python？",
    "Python 有什么特点？",
    "Python 的应用场景有哪些？",
    "Python 与 Java 有什么区别？",
    "Python 的发展历程是怎样的？",
]

results = chain.batch(questions)

for question, result in zip(questions, results):
    print(f"Question: {question}")
    print(f"Answer: {result.content}")
    print()
