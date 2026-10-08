from typing import Annotated
from typing_extensions import TypedDict

from langchain_core.messages import (
    HumanMessage,
    AIMessage,
)

from langgraph.graph import (
    StateGraph,
    START,
    END,
    add_messages,
)


# class State(TypedDict):
#     messages: Annotated[
#         list,
#         add_messages
#     ]

class State(TypedDict):
    messages: list


def node_a(state: State):
    return {
        "messages": [
            AIMessage(
                content="你好，我是 Agent。"
            )
        ]
    }


def node_b(state: State):
    return {
        "messages": [
            AIMessage(
                content="我可以帮你调用工具。"
            )
        ]
    }


builder = StateGraph(State)

builder.add_node("a", node_a)
builder.add_node("b", node_b)

builder.add_edge(START, "a")
builder.add_edge("a", "b")
builder.add_edge("b", END)

graph = builder.compile()


result = graph.invoke({
    "messages": [
        HumanMessage(
            content="你好"
        )
    ]
})

for message in result["messages"]:
    print(
        type(message).__name__,
        ":",
        message.content
    )
