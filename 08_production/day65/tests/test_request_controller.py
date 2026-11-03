import asyncio

from app.mock_llm import MockLLM
from app.request_controller import RequestController


def test_request_controller_limits_concurrency_and_retries():

    async def run_test():

        llm = MockLLM(fail_times=1)

        controller = RequestController(
            max_concurrency=2,
            requests_per_second=100,
        )

        async def task(i):
            return await controller.execute(
                lambda: llm.generate(f"task-{i}")
            )

        results = await asyncio.gather(
            *[task(i) for i in range(5)]
        )

        assert len(results) == 5

        assert llm.max_active <= 2

        # 5 次成功调用 + 1 次失败调用
        assert llm.call_count == 6

    asyncio.run(run_test())
