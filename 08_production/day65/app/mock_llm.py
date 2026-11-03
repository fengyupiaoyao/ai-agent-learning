import asyncio

from app.retry_handler import RateLimitError


class MockLLM:
    def __init__(self, fail_times=0):
        self.fail_times = fail_times
        self.call_count = 0
        self.active = 0
        self.max_active = 0

    async def generate(self, prompt):
        self.call_count += 1

        self.active += 1
        self.max_active = max(
            self.max_active,
            self.active,
        )

        try:
            print(f"LLM 请求: {prompt}")

            await asyncio.sleep(1)

            if self.fail_times > 0:
                self.fail_times -= 1
                raise RateLimitError(retry_after=1)

            return f"LLM 响应: {prompt}"
        finally:
            self.active -= 1
