import pytest

from app.faults import (
    FaultPlan,
    simulated_tool
)

from app.resilience import resilient_call


@pytest.mark.asyncio
async def test_tool_error_fallback():

    plan = FaultPlan(mode="tool_error")

    result = await resilient_call(
        lambda: simulated_tool(plan),
        fallback={"result": "fallback"}
    )

    assert result["status"] == "fallback"

    # 不可重试异常，不应该反复执行
    assert plan.calls == 1
