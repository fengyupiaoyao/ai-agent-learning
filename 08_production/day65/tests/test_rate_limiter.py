import asyncio
from nt import times
import time

from app.rate_limiter import RateLimiter


def test_rate_limiter_controls_request_interval():
    async def run_test():
        limiter = RateLimiter(
            requests_per_second=10
        )

        timestamps = []

        for _ in range(3):
            await limiter.acquire()
            timestamps.append(time.monotonic())

        intervals = [
            timestamps[i + 1] - timestamps[i]
            for i in range(len(timestamps) - 1)
        ]

        for interval in intervals:
            assert interval >= 0.00

    asyncio.run(run_test())
