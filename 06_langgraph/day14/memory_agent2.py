import os
from dotenv import load_dotenv
from rich.pretty import pprint

from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()

checkpointer = InMemorySaver()

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
            {"role": "user", "content": "我叫小明"},
        ]
    },
    config
)

pprint(response["messages"][-1].content)

response = agent.invoke(
    {
        "messages": [
            {"role": "user", "content": "我叫什么？"},
        ]
    },
    config
)
pprint(response["messages"][-1].content)
