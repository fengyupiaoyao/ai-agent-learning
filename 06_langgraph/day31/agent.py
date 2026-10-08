from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver


from state import State
from agent_node import agent_node
from route import should_continue
from tool_node import tool_node

checkpoint = InMemorySaver()

builder = StateGraph(State)
builder.add_node(
    "agent",
    agent_node
)
builder.add_node(
    "tools",
    tool_node
)

builder.add_edge(
    START,
    "agent"
)

builder.add_conditional_edges(
    "agent",
    should_continue,
    {
        "tools": "tools",
        END: END
    }
)

builder.add_edge(
    "tools",
    "agent"
)

graph = builder.compile(
    checkpoint
)
