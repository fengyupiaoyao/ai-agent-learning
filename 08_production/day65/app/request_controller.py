import asyncio

from app.rate_limiter import RateLimiter
from app.retry_handler import retry_async


class RequestController:
    def __init__(
        self,
        max_concurrency=3,
        requests_per_second=2,
    ):
        self.semaphore = asyncio.Semaphore(
            max_concurrency
        )

        self.rate_limiter = RateLimiter(
            requests_per_second
        )

    async def execute(self, func):
        async with self.semaphore:
            async def controlled_call():
                await self.rate_limiter.acquire()
                return await func()

            return await retry_async(
                controlled_call,
                max_retries=3,
            )
