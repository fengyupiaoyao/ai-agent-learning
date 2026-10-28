import asyncio


class ConcurrencyLimiter:
    def __init__(self, max_concurrency: int = 10):
        if max_concurrency < 1:
            raise ValueError("max_concurrency must be at least 1")
        self._semaphore = asyncio.Semaphore(max_concurrency)

    async def run(self, operation, *args, **kwargs):
        async with self._semaphore:
            return await operation(*args, **kwargs)
