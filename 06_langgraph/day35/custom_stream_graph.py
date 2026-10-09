from typing import TypedDict

from langgraph.graph import StateGraph, START, END
from rich import print as pprint

from custom_stream import search_node


class State(TypedDict):
    query: str
    documents: list[str]


builder = StateGraph(State)

builder.add_node("search", search_node)

builder.add_edge(START, "search")
builder.add_edge("search", END)

graph = builder.compile()


for chunk in graph.stream(
    {
        "query": "LangGraph custom stream 怎么使用",
        "documents": []
    },
    stream_mode="custom"
):
    pprint(chunk)
