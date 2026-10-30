import asyncio

import pytest

from app.reliability import (
    CircuitBreaker,
    CircuitBreakerOpen,
    CircuitState,
)


@pytest.mark.asyncio
async def test_circuit_breaker_opens_after_failures():
    breaker = CircuitBreaker(
        failure_threshold=2,
        recovery_timeout=10,
    )

    async def failing_service():
        raise RuntimeError("service unavailable")

    # 连续两次失败，达到熔断阈值
    for _ in range(2):
        with pytest.raises(RuntimeError):
            await breaker.call(failing_service)

    assert breaker.state == CircuitState.OPEN

    # 熔断期间直接拒绝请求
    with pytest.raises(CircuitBreakerOpen):
        await breaker.call(failing_service)


@pytest.mark.asyncio
async def test_circuit_breaker_recovers():
    breaker = CircuitBreaker(
        failure_threshold=1,
        recovery_timeout=0.01,
    )

    async def failing_service():
        raise RuntimeError("service unavailable")

    async def healthy_service():
        return "ok"

    with pytest.raises(RuntimeError):
        await breaker.call(failing_service)

    assert breaker.state == CircuitState.OPEN

    # 等待熔断恢复窗口结束
    await asyncio.sleep(0.02)

    result = await breaker.call(healthy_service)

    assert result == "ok"
    assert breaker.state == CircuitState.CLOSED
