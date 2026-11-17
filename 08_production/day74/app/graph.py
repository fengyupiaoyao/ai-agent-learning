from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from app.contracts import (
    HandoffEnvelope,
    ResearchResult,
    AnalysisResult,
    ReviewResult,
)

from app.agents import (
    researcher_agent,
    analyst_agent,
    reviewer_agent,
)

from app.handoff import (
    create_handoff,
    accept_handoff,
)


class HandoffState(TypedDict):
    task_id: str
    goal: str

    research: ResearchResult | None
    analysis: AnalysisResult | None
    review: ReviewResult | None

    current_handoff: HandoffEnvelope | None
    handoff_log: list[dict]

    status: str


def researcher_node(state: HandoffState):
    result = researcher_agent(state["goal"])

    return {
        "research": result,
        "status": "research_completed",
    }


def handoff_to_analyst_node(state: HandoffState):
    research = state["research"]

    envelope = create_handoff(
        task_id=state["task_id"],
        from_agent="researcher",
        to_agent="analyst",
        payload=research.model_dump(),
        context_summary=(
            "Researcher 已完成资料收集，"
            "请 Analyst 进行技术分析"
        )
    )

    return {
        "current_handoff": envelope,
        "status": "waiting_for_analyst",
    }


def analyst_node(state: HandoffState):
    envelope = state["current_handoff"]

    accepted = accept_handoff(
        envelope,
        receiver="analyst",
    )

    research = ResearchResult.model_validate(
        accepted.payload
    )

    result = analyst_agent(research)

    return {
        "analysis": result,
        "current_handoff": None,
        "handoff_log": (
            state["handoff_log"]
            + [accepted.model_dump(mode="json")]
        ),
        "status": "analysis_completed",
    }


def handoff_to_reviewer_node(state: HandoffState):
    analysis = state["analysis"]

    envelope = create_handoff(
        task_id=state["task_id"],
        from_agent="analyst",
        to_agent="reviewer",
        payload=analysis.model_dump(),
        context_summary=(
            "Analyst 已完成技术分析，"
            "请 Reviewer 进行审核"
        )
    )

    return {
        "current_handoff": envelope,
        "status": "waiting_for_reviewer",
    }


def reviewer_node(state: HandoffState):
    envelope = state["current_handoff"]

    accepted = accept_handoff(
        envelope,
        receiver="reviewer",
    )

    analysis = AnalysisResult.model_validate(
        accepted.payload
    )

    result = reviewer_agent(analysis)

    return {
        "review": result,
        "current_handoff": None,
        "handoff_log": (
            state["handoff_log"]
            + [accepted.model_dump(mode="json")]
        ),
        "status": (
            "completed"
            if result.approved
            else "rejected"
        ),
    }


builder = StateGraph(HandoffState)

builder.add_node("researcher", researcher_node)
builder.add_node(
    "handoff_to_analyst",
    handoff_to_analyst_node,
)
builder.add_node("analyst", analyst_node)
builder.add_node(
    "handoff_to_reviewer",
    handoff_to_reviewer_node,
)
builder.add_node("reviewer", reviewer_node)

builder.add_edge(START, "researcher")
builder.add_edge("researcher", "handoff_to_analyst")
builder.add_edge("handoff_to_analyst", "analyst")
builder.add_edge("analyst", "handoff_to_reviewer")
builder.add_edge("handoff_to_reviewer", "reviewer")
builder.add_edge("reviewer", END)

graph = builder.compile()
