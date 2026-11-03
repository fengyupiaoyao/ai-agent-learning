import asyncio

from app.database import Database
from app.task_repository import TaskRepository
from app.task_executor import TaskExecutor
from app.mock_agent import MockAgent


def test_duplicate_request_only_executes_once():

    async def run_test():

        database = Database(":memory:")

        repository = TaskRepository(database)
        agent = MockAgent()

        executor = TaskExecutor(
            repository,
            agent,
        )

        result1 = await executor.execute(
            "user_001",
            "key-001",
            "研究 LangGraph",
        )

        result2 = await executor.execute(
            "user_001",
            "key-001",
            "研究 LangGraph",
        )

        assert result1["status"] == "succeeded"
        assert result2["status"] == "succeeded"

        assert result1["duplicate"] is False
        assert result2["duplicate"] is True

        assert agent.call_count == 1

        database.close()

    asyncio.run(run_test())


def test_same_key_with_different_request_is_rejected():

    async def run_test():

        database = Database(":memory:")

        repository = TaskRepository(database)
        agent = MockAgent()

        executor = TaskExecutor(
            repository,
            agent,
        )

        await executor.execute(
            "user_001",
            "key-002",
            "研究 LangGraph",
        )

        try:
            await executor.execute(
                "user_001",
                "key-002",
                "研究 LangChain",
            )
            assert False, "应该拒绝不同请求"

        except ValueError as exc:
            assert "不同请求" in str(exc)

        assert agent.call_count == 1

        database.close()

    asyncio.run(run_test())


def test_different_users_can_use_same_key():

    async def run_test():

        database = Database(":memory:")

        repository = TaskRepository(database)
        agent = MockAgent()

        executor = TaskExecutor(
            repository,
            agent,
        )

        result1 = await executor.execute(
            "user_001",
            "same-key",
            "研究 LangGraph",
        )

        result2 = await executor.execute(
            "user_002",
            "same-key",
            "研究 LangGraph",
        )

        assert result1["task_id"] != result2["task_id"]
        assert agent.call_count == 2

        database.close()

    asyncio.run(run_test())
