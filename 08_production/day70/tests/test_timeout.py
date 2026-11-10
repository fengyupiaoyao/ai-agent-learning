import pytest

from app.faults import simulated_tool, FaultPlan
from app.resilience import resilient_call


@pytest.mark.asyncio
async def test_timeout_fallback():
    plan = FaultPlan(mode="timeout")

    result = await resilient_call(
        lambda: simulated_tool(plan),
        timeout=0.05,
        max_retries=2,
        fallback={"result": "fallback"}
    )

    assert result["status"] == "fallback"
    assert plan.calls == 3
