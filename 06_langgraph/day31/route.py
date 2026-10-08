from langgraph.graph import END
from state import State


def should_continue(state: State):
    last_message = state["messages"][-1]

    if last_message.tool_calls:
        return "tools"

    return END
