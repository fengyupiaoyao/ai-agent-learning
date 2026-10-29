import asyncio
import pytest

from app.services.research_service import (
    AgentTimeoutError,
    ResearchService,
)

from app.core.rate_limit import RateLimiter


class SlowAgent:
    async def ainvoke(self, payload):
        await asyncio.sleep(1)
        return {"messages": []}


@pytest.mark.asyncio
async def test_agent_timeout():
    service = ResearchService(
        agent=SlowAgent(),
        timeout_seconds=0.05,
    )

    with pytest.raises(AgentTimeoutError):
        await service.run("测试超时")


@pytest.mark.asyncio
async def test_rate_limiter():
    limiter = RateLimiter(
        max_requests=2,
        window_seconds=60,
    )

    assert await limiter.allow("user-a")
    assert await limiter.allow("user-a")
    assert not await limiter.allow("user-a")

    # 不同 key 的计数相互独立
    assert await limiter.allow("user-b")
