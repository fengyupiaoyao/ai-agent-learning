from typing import Annotated
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END


def merge_numbers(
    old: list[int],
    new: list[int]
) -> list[int]:
    return old + new


class State(TypedDict):
    numbers: Annotated[
        list[int],
        merge_numbers
    ]


def node_a(state: State):
    return {
        "numbers": [1, 2, 3]
    }


def node_b(state: State):
    return {
        "numbers": [4, 5, 6]
    }


builder = StateGraph(State)

builder.add_node("a", node_a)
builder.add_node("b", node_b)

builder.add_edge(START, "a")
builder.add_edge("a", "b")
builder.add_edge("b", END)

graph = builder.compile()

result = graph.invoke({
    "numbers": [0]
})

print(result)
