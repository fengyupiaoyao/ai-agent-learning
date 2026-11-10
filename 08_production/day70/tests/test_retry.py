import pytest

from app.faults import simulated_tool, FaultPlan
from app.resilience import resilient_call


@pytest.mark.asyncio
async def test_retry_success():
    plan = FaultPlan(
        mode="network",
        fail_times=2
    )

    result = await resilient_call(
        lambda: simulated_tool(plan),
        timeout=0.5,
        max_retries=2
    )

    assert result["status"] == "success"
    assert plan.calls == 3
