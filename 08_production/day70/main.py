import asyncio
import logging

from app.agent import ReliabilityAgent
from app.faults import FaultPlan

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)


async def main():
    agent = ReliabilityAgent()

    scenarios = [
        ("task-001", FaultPlan("normal")),
        ("task-002", FaultPlan("timeout")),
        ("task-003", FaultPlan("network", 2)),
        ("task-004", FaultPlan("tool_error"))
    ]

    for task_id, plan in scenarios:
        print(f"\nRunning {task_id}")

        result = await agent.run(task_id, plan)

        print(result)

if __name__ == "__main__":
    asyncio.run(main())
