import pytest

from app.services.research_service import ResearchService
from tests.fakes import FakeAgent


@pytest.mark.asyncio
async def test_research_returns_agent_answer():
    service = ResearchService(agent=FakeAgent())

    result = await service.research("What is the capital of France?")

    assert result == "Research result: What is the capital of France?"
