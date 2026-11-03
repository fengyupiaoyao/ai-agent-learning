import asyncio

from langchain_classic.agents import agent

from app.database import Database
from app.task_repository import TaskRepository
from app.task_executor import TaskExecutor
from app.mock_agent import MockAgent

async def main():
    database = Database()

    repository = TaskRepository(database)

    agent = MockAgent()

    executor = TaskExecutor(repository, agent)

    user_id = "user_001"

    result1 = await executor.execute(
        user_id=user_id,
        idempotency_key="research-001",
        prompt="研究 LangGraph",
    )

    print("\n第一次提交：")
    print(result1)

    result2 = await executor.execute(
        user_id=user_id,
        idempotency_key="research-001",
        prompt="研究 LangGraph",
    )

    print("\n第二次提交：")
    print(result2)

    print("\nAgent 实际执行次数：")
    print(agent.call_count)

    database.close()

if __name__ == "__main__":
    asyncio.run(main())