from app.orchestrator import AgentOrchestrator


def test_normal_task_completed():
    agent = AgentOrchestrator()

    result = agent.run(
        task_id="test-001",
        user_input="分析 Agent 架构",
    )

    assert result["status"] == "completed"
    assert result["plan"]
    assert result["results"]


def test_dangerous_task_requires_approval():
    agent = AgentOrchestrator()

    result = agent.run(
        task_id="test-002",
        user_input="删除旧文件",
        approved=False,
    )

    assert result["status"] == "rejected"
