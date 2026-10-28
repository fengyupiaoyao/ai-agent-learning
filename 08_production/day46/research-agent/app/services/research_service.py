import logging
import time
import asyncio

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model

from app.agents.research_agent import build_research_agent

from app.core.limits import ConcurrencyLimiter

logger = logging.getLogger(__name__)


class AgentTimeoutError(Exception):
    """Error raised when the agent takes too long to respond."""


class ResearchService:
    def __init__(self, agent=None, timeout_seconds: int = 30):
        self.agent = agent or build_research_agent()
        self.timeout_seconds = timeout_seconds
        self.concurrency_limiter = ConcurrencyLimiter(max_concurrency=10)

    async def run(self, question: str) -> str:
        started = time.perf_counter()

        logger.info("agent_run_started")

        try:
            async def invoke():
                async with asyncio.timeout(self.timeout_seconds):
                    return await self.agent.ainvoke(
                        {
                            "messages": [
                                {"role": "user", "content": question}
                            ]
                        }
                    )

            result = await self.concurrency_limiter.run(invoke)

            messages = result["messages"]
            if not messages:
                raise ValueError("No messages in result")

            content = messages[-1].content
            if isinstance(content, str):
                answer = content
            else:
                answer = str(content)

            elapsed = (time.perf_counter() - started) * 1000
            logger.info(
                "agent_run_completed duration_ms=%.2f",
                elapsed,
            )
            return answer
        except TimeoutError as exc:
            elapsed = (time.perf_counter() - started) * 1000
            logger.warning(
                "agent_run_timed_out duration_ms=%.2f",
                elapsed,
            )
            raise AgentTimeoutError("Agent timed out") from exc
