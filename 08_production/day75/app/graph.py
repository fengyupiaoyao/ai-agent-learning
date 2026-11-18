from langgraph.graph import StateGraph, START, END
from langgraph.types import Send

from app.state import State
from app.researcher import research_worker
from app.merger import merge_results


def dispatch_research(state: State) -> list[Send]:
    """把每个研究主题分发给一个 Worker。"""
    return [
        Send(
            "research_worker",
            {
                "topic": topic
            }
        )
        for topic in state["topics"]
    ]


def build_graph():
    builder = StateGraph(State)

    builder.add_node("dispatch_research", dispatch_research)
    builder.add_node("research_worker", research_worker)
    builder.add_node("merge_results", merge_results)

    builder.add_conditional_edges(
        START,
        dispatch_research,
        ["research_worker"],
    )

    builder.add_edge("research_worker", "merge_results")

    builder.add_edge("merge_results", END)

    return builder.compile()


graph = build_graph()
