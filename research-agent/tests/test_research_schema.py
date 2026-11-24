import pytest
from pydantic import ValidationError

from app.schemas.research import (
    ResearchRequest,
    ResearchResponse,
    ResearchStatus,
)


def test_research_request_default():
    request = ResearchRequest(
        question="研究 LangGraph 的工作原理"
    )

    assert request.max_steps == 5
    assert request.use_knowledge_base is True
    assert request.use_web_search is True


def test_research_request_invalid_question():

    with pytest.raises(ValidationError):
        ResearchRequest(question="AI")


def test_research_request_max_steps():

    with pytest.raises(ValidationError):
        ResearchRequest(
            question="研究 LangGraph",
            max_steps=30
        )


def test_research_status():

    assert ResearchStatus.PENDING == "pending"
    assert ResearchStatus.RUNNING == "running"
    assert ResearchStatus.COMPLETED == "completed"
    assert ResearchStatus.FAILED == "failed"
