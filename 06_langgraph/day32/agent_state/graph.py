from langgraph.graph import (
    StateGraph,
    START,
    END,
)

from langgraph.prebuilt import (
    ToolNode,
    tools_condition,
)

from state import AgentState
from nodes import agent_node
from tools import tools


builder = StateGraph(AgentState)


builder.add_node(
    "agent",
    agent_node
)

builder.add_node(
    "tools",
    ToolNode(tools)
)


builder.add_edge(
    START,
    "agent"
)


builder.add_conditional_edges(
    "agent",
    tools_condition,
    {
        "tools": "tools",
        END: END,
    }
)


builder.add_edge(
    "tools",
    "agent"
)


graph = builder.compile()
