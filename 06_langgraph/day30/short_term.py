from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver


builder = StateGraph(AgentState)

builder.add_node(
    "model",
    call_model
)

builder.add_edge(
    START,
    "model"
)

builder.add_edge(
    "model",
    END
)

checkpointer = InMemorySaver()

graph = builder.compile(
    checkpointer=checkpointer
)
