import asyncio
import time


class RateLimiter:
    def __init__(self, requests_per_second: float):
        if requests_per_second <= 0:
            raise ValueError("requests_per_second must be greater than zero")

        self.interval = 1.0 / requests_per_second
        self.lock = asyncio.Lock()
        self.next_allowed_time = 0.0

    async def acquire(self):
        async with self.lock:
            now = time.monotonic()

            wait_time = max(
                0.0,
                self.next_allowed_time - now
            )

            if wait_time > 0:
                await asyncio.sleep(wait_time)

            self.next_allowed_time = (
                max(time.monotonic(), self.next_allowed_time) + self.interval
            )
