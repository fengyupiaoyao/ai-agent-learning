import asyncio

from app.mock_llm import MockLLM
from app.request_controller import RequestController


async def main():
    llm = MockLLM(fail_times=2)

    controller = RequestController(
        max_concurrency=3,
        requests_per_second=2,
    )

    async def task(prompt):
        result = await controller.execute(
            lambda: llm.generate(prompt)
        )

        print("执行结果: ", result)

        return result

    prompts = [
        f"Research Task {i}"
        for i in range(1, 7)
    ]

    results = await asyncio.gather(
        *[
            task(prompt)
            for prompt in prompts
        ]
    )

    print("\n=== 执行统计 ===")
    print("成功任务数：", len(results))
    print("实际 API 调用次数：", llm.call_count)
    print("最大并发数：", llm.max_active)

if __name__ == "__main__":
    asyncio.run(main())
