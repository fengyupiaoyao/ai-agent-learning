from app.graph import build_graph


def test_dynamic_replanning():

    graph = build_graph()

    initial_state = {
        "goal": "AI Agent 技术研究",
        "tasks": [],
        "current_index": 0,
        "results": [],
        "replan_count": 0,
        "max_replans": 3,
        "current_result": "",
        "current_error": "",
        "status": "pending",
        "fail_task_id": "task_2"
    }

    result = graph.invoke(initial_state)

    assert result["status"] == "evaluated" or (
        result["current_index"] == len(result["tasks"])
    )

    assert result["replan_count"] == 1

    assert all(
        task["status"] == "completed"
        for task in result["tasks"]
    )
