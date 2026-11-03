import asyncio
import random


class RateLimitError(Exception):
    def __init__(self, message="Rate limit exceeded", retry_after=None):
        super().__init__(message)
        self.retry_after = retry_after


async def retry_async(
    func,
    max_retries=3,
    base_delay=1,
    max_delay=30,
):
    for attempt in range(max_retries + 1):
        try:
            return await func()

        except RateLimitError as e:
            if attempt >= max_retries:
                raise

            exponential_delay = min(
                max_delay,
                base_delay * (2 ** attempt)
            )

            jitter = random.uniform(0, 0.5)

            delay = exponential_delay + jitter

            if e.retry_after is not None:
                delay = max(delay, e.retry_after)

            await asyncio.sleep(delay)
