from typing import TypedDict

from langgraph.graph import (
    StateGraph,
    START,
    END,
)

from app.contracts import (
    ResearchOutput,
    AnalysisOutput,
    ReviewOutput,
)

from app.agents import (
    research_agent,
    analysis_agent,
    review_agent,
)

MAX_REVIEW_ROUNDS = 2


class MultiAgentState(TypedDict):
    goal: str
    research: ResearchOutput | None
    analysis: AnalysisOutput | None
    review: ReviewOutput | None
    review_round: int
    status: str


def research_node(state: MultiAgentState):
    result = research_agent(state["goal"])

    return {
        "research": result,
        "status": "research_completed",
    }


def analyst_node(state: MultiAgentState):
    result = analysis_agent(state["research"])

    return {
        "analysis": result,
        "status": "analysis_completed",
    }


def reviewer_node(state: MultiAgentState):
    result = review_agent(state["analysis"])

    return {
        "review": result,
        "review_round": state["review_round"] + 1,
        "status": (
            "approved"
            if result.approved
            else "rejected"
        )
    }


def route_after_review(state: MultiAgentState):
    review = state["review"]

    if review is None:
        return END

    if review.approved:
        return END

    if state["review_round"] >= MAX_REVIEW_ROUNDS:
        return END

    return "analyst"


builder = StateGraph(MultiAgentState)

builder.add_node("research", research_node)
builder.add_node("analyst", analyst_node)
builder.add_node("reviewer", reviewer_node)

builder.add_edge(START, "research")
builder.add_edge("research", "analyst")
builder.add_edge("analyst", "reviewer")

builder.add_conditional_edges(
    "reviewer",
    route_after_review,
    {
        "analyst": "analyst",
        END: END,
    },
)

graph = builder.compile()
