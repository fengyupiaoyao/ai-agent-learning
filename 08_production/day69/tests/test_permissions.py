import pytest

from app.models import UserContext, ToolCall
from app.tool_router import ToolRouter


@pytest.fixture
def router():
    return ToolRouter()


def test_viewer_can_search(router):
    user = UserContext("u1", "viewer")

    result = router.execute(
        user,
        ToolCall("search_docs", {"query": "Agent"}),
    )

    assert result.success is True


def test_viewer_cannot_delete_file(router):
    user = UserContext("u1", "viewer")

    result = router.execute(
        user,
        ToolCall("delete_file", {"file_id": "f1"}),
    )

    assert result.success is False
    assert result.error == "Permission denied"


def test_researcher_can_read_file(router):
    user = UserContext("u2", "researcher")

    result = router.execute(
        user,
        ToolCall("read_file", {"file_id": "f1"}),
    )

    assert result.success is True


def test_unknown_tool_is_rejected(router):
    user = UserContext("u1", "admin")

    result = router.execute(
        user,
        ToolCall("execute_shell", {"command": "whoami"}),
    )

    assert result.success is False
    assert result.error == "Tool not found"


def test_extra_arguments_are_rejected(router):
    user = UserContext("u2", "researcher")

    result = router.execute(
        user,
        ToolCall(
            "read_file",
            {
                "file_id": "f1",
                "admin": True,
            },
        ),
    )

    assert result.success is False
    assert result.error == "Invalid arguments"


def test_high_risk_tool_requires_approval(router):
    user = UserContext("u3", "operator")

    result = router.execute(
        user,
        ToolCall(
            "send_email",
            {
                "to": "test@example.com",
                "subject": "Test",
                "body": "Hello",
            },
        ),
    )

    assert result.success is False
    assert result.requires_approval is True


def test_approved_high_risk_tool_can_execute(router):
    user = UserContext("u3", "operator")

    router.approval.approve("approval_001")

    result = router.execute(
        user,
        ToolCall(
            "send_email",
            {
                "to": "test@example.com",
                "subject": "Test",
                "body": "Hello",
            },
        ),
        approval_id="approval_001",
    )

    assert result.success is True
