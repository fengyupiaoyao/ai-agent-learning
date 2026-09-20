import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI


class MovieReview(BaseModel):
    title: str = Field(description="电影名称")
    score: float = Field(description="电影评分，范围 0 到 10")
    sentiment: str = Field(description="情感倾向，例如 positive、neutral、negative")
    summary: str = Field(description="电影评价总结")


load_dotenv(Path(__file__).resolve().parents[1] / ".env")

model = ChatOpenAI(
    model="qwen-plus",
    api_key=os.environ["OPENAI_API_KEY"],
    base_url="https://ws-wopagvlf3afu5baf.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

structured_model = model.with_structured_output(MovieReview)

result = structured_model.invoke(
    """
    请分析电影《星际穿越》。

    请给出电影名称、评分、情感倾向和评价总结。
    """
)

print(result)
print(type(result))
print(result.title)
print(result.score)
print(result.sentiment)
print(result.summary)
