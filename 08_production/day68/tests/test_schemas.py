import pytest

from pydantic import ValidationError
from app.schemas import AgentRequest


def test_valid_request():
    request = AgentRequest(
        user_id="user_001",
        question="总结文档",
    )

    assert request.user_id == "user_001"


def test_invalid_user_id():
    with pytest.raises(ValidationError):
        AgentRequest(
            user_id="user@001",
            question="总结文档",
        )


def test_question_too_long():
    with pytest.raises(ValidationError):
        AgentRequest(
            user_id="user_001",
            question="A" * 2001,
        )


def test_extra_field_rejected():
    with pytest.raises(ValidationError):
        AgentRequest(
            user_id="user_001",
            question="总结文档",
            is_admin=True,
        )
