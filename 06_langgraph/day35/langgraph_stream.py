from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from rich import print as pprint


class State(TypedDict):
    count: int


def add_one(state: State) -> State:
    state["count"] += 1
    return state


def add_two(state: State) -> State:
    state["count"] += 2
    return state


builder = StateGraph(State)

builder.add_node("add_one", add_one)
builder.add_node("add_two", add_two)

builder.add_edge(START, "add_one")
builder.add_edge("add_one", "add_two")
builder.add_edge("add_two", END)

graph = builder.compile()

# result = graph.invoke({"count": 0})

# pprint(result)

# for chunk in graph.stream(
#     {"count": 0},
#     stream_mode="values"
# ):
#     pprint(chunk)

for chunk in graph.stream(
    {"count": 0},
    stream_mode="updates"
):
    pprint(chunk)
