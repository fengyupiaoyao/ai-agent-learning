from langchain_openai import ChatOpenAI

from state import AgentState
from tools import tools

import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(
    model="qwen3.8-max",
    api_key=os.environ["OPENAI_API_KEY"],
    base_url="https://ws-wopagvlf3afu5baf.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
    temperature=0,
)

llm_with_tools = llm.bind_tools(tools)


def agent_node(state: AgentState):
    response = llm_with_tools.invoke(state["messages"])

    return {
        "messages": [response]
    }
