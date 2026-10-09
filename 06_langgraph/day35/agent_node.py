from typing import TypedDict, Annotated
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages

from langchain_openai import ChatOpenAI

import os
from dotenv import load_dotenv

load_dotenv()


class State(TypedDict):
    messages: Annotated[
        list[AnyMessage],
        add_messages
    ]


llm = ChatOpenAI(
    model="qwen3.8-max",
    api_key=os.environ["OPENAI_API_KEY"],
    base_url="https://ws-wopagvlf3afu5baf.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
    temperature=0,
)


def agent_node(state: State):
    response = llm.invoke(
        state["messages"]
    )

    return {
        "messages": [response]
    }
