import asyncio

class MockAgent:
    def __init__(self):
        self.call_count = 0

    async def run(self, prompt):
        self.call_count += 1

        print(f"Agent 正在执行：{prompt}")

        await asyncio.sleep(1)

        return {
            "report": f"Research result for: {prompt}"
        }