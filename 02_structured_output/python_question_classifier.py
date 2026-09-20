import os
from pathlib import Path
from dotenv import load_dotenv

from typing import List

from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# 按脚本位置加载项目根目录的配置，不依赖运行目录
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

model = ChatOpenAI(
    model="qwen-plus",
    api_key=os.environ["OPENAI_API_KEY"],
    base_url="https://ws-wopagvlf3afu5baf.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)


class QuestionAnalysis(BaseModel):
    topic: str = Field(
        description="Python 问题所属主题，例如 asyncio、OOP、decorator、database"
    )

    difficulty: str = Field(
        description="问题难度，只能是 easy、medium、hard"
    )

    question_type: str = Field(
        description="问题类型，例如 concept、debug、implementation、comparison"
    )

    keywords: List[str] = Field(
        description="问题中的关键技术关键词"
    )

    answer: str = Field(
        description="问题的简洁答案"
    )


prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        你是一名 Python 技术面试专家。

        请分析用户提出的 Python 问题，
        并严格按照要求的结构返回结果。
        """
    ),
    (
        "human",
        "{question}"
    )
])

structured_model = model.with_structured_output(QuestionAnalysis)

chain = prompt | structured_model

question = input("请输入 Python 问题: ")

result = chain.invoke({"question": question})

print("\n分析结果")
print("=" * 40)

print("主题:", result.topic)
print("难度:", result.difficulty)
print("类型:", result.question_type)
print("关键词:", result.keywords)
print("答案:", result.answer)
