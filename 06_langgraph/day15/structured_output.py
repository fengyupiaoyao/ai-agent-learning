import os
from turtle import st
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from rich.pretty import pprint

from langchain.chat_models import init_chat_model
from langchain.agents import create_agent

load_dotenv()

model = init_chat_model(
    # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    "openai:qwen3.8-max",
    api_key=os.environ["OPENAI_API_KEY"],
    base_url="https://ws-wopagvlf3afu5baf.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
    temperature=0.5,
    timeout=300,
    max_tokens=25000,
)

agent = create_agent(
    model=model,
    tools=[],
)


class UserInfo(BaseModel):
    name: str = Field(
        description="The user's name"
    )

    age: int = Field(
        description="The user's age"
    )

    city: str = Field(
        description="The user's city"
    )


structured_model = model.with_structured_output(UserInfo)

response = structured_model.invoke("我叫 Jack，今年 28 岁，现在住在东京.")

pprint(response)
print(type(response))
