from state import State
from llm import llm_with_tools


def agent_node(state: State):
    response = llm_with_tools.invoke(state["messages"])
    return {
        "messages": [response]
    }
