import logging
import time

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model

from app.agents.research_agent import build_research_agent

logger = logging.getLogger(__name__)


class ResearchService:
    def __init__(self, agent=None):
        self.agent = agent or build_research_agent()

    async def run(self, question: str) -> str:
        started = time.perf_counter()

        logger.info("agent_run_started")

        try:
            result = await self.agent.ainvoke(
                {
                    "messages": [
                        {"role": "user", "content": question}
                    ]
                }
            )

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
                elapsed_ms,
            )
            return answer
        except Exception as e:
            elapsed_ms = (time.perf_counter() - started) * 1000
            logger.exception(
                "agent_run_failed duration_ms=%.2f",
                elapsed_ms,
            )
            raise
