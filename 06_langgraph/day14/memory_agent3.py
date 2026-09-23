import os
from dotenv import load_dotenv
from rich.pretty import pprint
from langchain.tools import tool

from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()

checkpointer = InMemorySaver()


@tool
def get_weather(city: str) -> str:
    """Get the weather for a city."""
    weather = {
        "Tokyo": "Sunny, 25°C",
        "Beijing": "Cloudy, 22°C",
        "Shanghai": "Rainy, 20°C",
    }
    return weather.get(city, "Unknown city")


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
    tools=[get_weather],
    checkpointer=checkpointer,
)

config = {
    "configurable": {
        "thread_id": "user_001"
    }
}

response = agent.invoke(
    {
        "messages": [
            {"role": "user", "content": "我住在东京"},
        ]
    },
    config
)

pprint(response["messages"][-1].content)

response = agent.invoke(
    {
        "messages": [
            {"role": "user", "content": "今天那里的天气怎么样？"},
        ]
    },
    config
)
pprint(response["messages"][-1].content)
