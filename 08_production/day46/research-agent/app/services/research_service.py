from langchain.agents import create_agent
from langchain.chat_models import init_chat_model

from app.agents.research_agent import build_research_agent


class ResearchService:
    def __init__(self, agent=None):
        self.agent = agent or build_research_agent()

    async def run(self, question: str) -> str:
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
            return content

        return str(content)
