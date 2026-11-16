from app.planner import planner_node


def test_planner():

    state = {
        "goal": "AI Agent 技术研究"
    }

    result = planner_node(state)

    assert len(result["tasks"]) == 4

    assert result["tasks"][0]["status"] == "pending"
