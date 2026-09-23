import os
from dotenv import load_dotenv
from rich.pretty import pprint

from langchain.chat_models import init_chat_model
from langchain.agents import create_agent

from langchain_core.tools import tool


@tool
def add(a: int, b: int) -> int:
    """Add two integers."""
    return a + b


@tool
def multiply(a: int, b: int) -> int:
    """Multiply two integers."""
    return a * b


@tool
def get_weather(city: str) -> str:
    # """Get the weather for a city."""
    """Calculate the price of a product."""
    weather_data = {
        "Tokyo": "Sunny, 25°C",
        "Beijing": "Cloudy, 22°C",
        "Shanghai": "Rainy, 20°C",
    }
    return weather_data.get(city, "City not found")


load_dotenv()

model = init_chat_model(
    # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    "openai:qwen3.7-plus",
    api_key=os.environ["OPENAI_API_KEY"],
    base_url="https://ws-wopagvlf3afu5baf.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
    temperature=0.5,
    timeout=300,
    max_tokens=25000,
)

agent = create_agent(
    model=model,
    tools=[
        add,
        multiply,
        get_weather,
    ],
)

response = agent.invoke(
    {
        "messages": [
            {"role": "user", "content": "东京今天天气怎么样"},
        ]
    }
)

pprint(response)
