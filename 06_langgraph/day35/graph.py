from langgraph.graph import StateGraph, START, END
from agent_node import agent_node
from agent_node import State
from langchain_core.messages import HumanMessage
from rich import print as pprint

builder = StateGraph(State)

builder.add_node("agent", agent_node)

builder.add_edge(START, "agent")
builder.add_edge("agent", END)

graph = builder.compile()

# for chunk in graph.stream(
#     {
#         "messages": [
#             HumanMessage(content="Hello, how are you?")
#         ]
#     },
#     stream_mode="messages"
# ):
#     pprint(chunk)

for chunk in graph.stream(
    {
        "messages": [
            HumanMessage(content="Hello, how are you?")
        ]
    },
    stream_mode="custom"
):
    pprint(chunk)
