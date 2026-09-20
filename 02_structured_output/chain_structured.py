import os
from pathlib import Path
from dotenv import load_dotenv

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
        description="问题所属主题"
    )

    difficulty: str = Field(
        description="问题难度，例如 easy、medium、hard"
    )

    answer: str = Field(
        description="问题的简洁答案"
    )


prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "你是一名 Python 专家，请分析用户的问题。"
    ),
    (
        "human",
        "{question}"
    )
])

structured_model = model.with_structured_output(QuestionAnalysis)

chain = prompt | structured_model

result = chain.invoke({"question": "Python 中 async 和 await 是什么？"})

print(result)

print("主题:", result.topic)
print("难度:", result.difficulty)
print("答案:", result.answer)
