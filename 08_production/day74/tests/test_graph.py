from app.graph import graph


def test_complete_handoff_workflow():
    result = graph.invoke({
        "task_id": "task-001",
        "goal": "研究 LangChain 和 LangGraph",

        "research": None,
        "analysis": None,
        "review": None,

        "current_handoff": None,
        "handoff_log": [],

        "status": "started",
    })

    assert result["status"] == "completed"

    assert result["analysis"] is not None
    assert result["review"].approved is True

    assert len(result["handoff_log"]) == 2

    assert (
        result["handoff_log"][0]["from_agent"]
        == "researcher"
    )

    assert (
        result["handoff_log"][0]["to_agent"]
        == "analyst"
    )

    assert (
        result["handoff_log"][1]["from_agent"]
        == "analyst"
    )

    assert (
        result["handoff_log"][1]["to_agent"]
        == "reviewer"
    )
