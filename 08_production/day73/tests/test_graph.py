from app.graph import (
    graph,
    route_after_review,
)
from app.contracts import ReviewOutput


def test_multi_agent_workflow():
    result = graph.invoke({
        "goal": "研究 LangChain 和 LangGraph",
        "research": None,
        "analysis": None,
        "review": None,
        "review_round": 0,
        "status": "started",
    })

    assert result["research"] is not None
    assert result["analysis"] is not None
    assert result["review"].approved is True
    assert result["status"] == "approved"


def test_review_max_rounds():
    state = {
        "goal": "test",
        "research": None,
        "analysis": None,
        "review": ReviewOutput(
            approved=False,
            score=40,
            feedback="需要补充",
        ),
        "review_round": 2,
        "status": "rejected",
    }

    assert route_after_review(state) == "__end__"


def test_review_rejected_loops_back():
    state = {
        "goal": "test",
        "research": None,
        "analysis": None,
        "review": ReviewOutput(
            approved=False,
            score=40,
            feedback="需要补充",
        ),
        "review_round": 0,
        "status": "rejected",
    }

    assert route_after_review(state) == "analyst"


def test_review_missing_ends():
    state = {
        "goal": "test",
        "research": None,
        "analysis": None,
        "review": None,
        "review_round": 0,
        "status": "started",
    }

    assert route_after_review(state) == "__end__"
