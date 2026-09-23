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
def subtract(a: int, b: int) -> int:
    """Subtract b from a."""
    return a - b


@tool
def search_product(product: str) -> str:
    """Search product information."""

    products = {
        "iPhone": "iPhone 17, price 799 USD",
        "MacBook": "MacBook Air, price 999 USD",
        "iPad": "iPad Air, price 599 USD",
    }

    return products.get(
        product,
        "Product not found"
    )


@tool
def calculate_discount(price: float, discount: float) -> float:
    """Calculate the final price after discount."""

    return price * (1 - discount)


@tool
def get_weather(city: str) -> str:
    """Get the weather for a city."""
    # """Calculate the price of a product."""
    weather_data = {
        "Tokyo": "Sunny, 25°C",
        "Beijing": "Cloudy, 22°C",
        "Shanghai": "Rainy, 20°C",
    }
    return weather_data.get(city, "City not found")


@tool
def get_status() -> str:
    """Get the current system status."""
    return "System is running normally."


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
    tools=[
        add,
        multiply,
        subtract,
        get_weather,
        search_product,
        calculate_discount,
        get_status,
    ],
)

response = agent.invoke(
    {
        "messages": [
            # {"role": "user", "content": "先计算 123 + 456，然后把结果乘以 2。"},
            # {"role": "user", "content": "查询 iPhone 的价格，然后计算打 10% 折扣后的价格。"},
            {"role": "user", "content": "告诉我系统状态。"},
        ]
    }
)

pprint(response)
