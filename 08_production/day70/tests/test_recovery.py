import pytest

from app.agent import ReliabilityAgent
from app.faults import FaultPlan


@pytest.mark.asyncio
async def test_checkpoint_recovery():

    agent = ReliabilityAgent()

    plan = FaultPlan(mode="normal")

    # 第一次执行
    result1 = await agent.run("task-001", plan)

    assert result1["status"] == "completed"

    calls_after_first = plan.calls

    # 第二次执行同一个已完成任务
    result2 = await agent.run("task-001", plan)

    assert result2["status"] == "completed"

    # 不应该重复执行工具
    assert plan.calls == calls_after_first
