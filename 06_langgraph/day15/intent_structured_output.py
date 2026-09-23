import os
from typing import Literal
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


class UserIntent(BaseModel):
    intent: Literal[
        "weather",
        "search",
        "calculation",
        "other",
    ] = Field(
        description="The user's intent"
    )

    city: str | None = Field(
        default=None,
        description="The city mentioned by the user"
    )

    date: str | None = Field(
        default=None,
        description="The date mentioned by the user"
    )


def route_intent(intent: UserIntent):
    if intent.intent == "weather":
        return "weather_tool"

    if intent.intent == "calculation":
        return "calculator_tool"

    if intent.intent == "search":
        return "search_tool"

    return "no_tool"


structured_model = model.with_structured_output(UserIntent)

questions = [
    "帮我查询东京明天的天气",
    "帮我搜索 LangChain Agent 的官方文档",
    "计算 123 加 456",
    "你好，今天心情不错",
]

for question in questions:
    response = structured_model.invoke(question)

    next_step = route_intent(response)

    pprint(f"Question: {question}")
    pprint(f"Response: {response}")
    pprint(f"Next Step: {next_step}")
    print("=" * 50)
