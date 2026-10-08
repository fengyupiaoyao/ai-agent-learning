from typing import TypedDict

from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    message: str


def hello(state: State):
    print("Hello Node")

    return {
        "message": state["message"] + " World"
    }


def node_a(state: State):
    print("Node A")
    return {
        "message": state["message"] + " from Node A"
    }


def node_b(state: State):
    print("Node B")
    return {
        "message": state["message"] + " from Node B"
    }


builder = StateGraph(State)

builder.add_node(
    "hello",
    hello
)
builder.add_node(
    "node_a",
    node_a
)
builder.add_node(
    "node_b",
    node_b
)

builder.add_edge(
    START,
    "hello"
)

builder.add_edge(
    "hello",
    "node_a"
)
builder.add_edge(
    "node_a",
    "node_b"
)

builder.add_edge(
    "node_b",
    END
)

graph = builder.compile()


result = graph.invoke({
    "message": "Hello"
})

print(result)
