import pytest

from app.handoff import (
    create_handoff,
    accept_handoff,
    reject_handoff,
    HandoffError,
)


def make_handoff():
    return create_handoff(
        task_id="task-001",
        from_agent="researcher",
        to_agent="analyst",
        payload={
            "topic": "LangGraph",
            "findings": ["资料 A", "资料 B"],
        },
        context_summary="研究资料已经收集完成",
    )


def test_create_handoff():
    handoff = make_handoff()

    assert handoff.status == "pending"
    assert handoff.from_agent == "researcher"
    assert handoff.to_agent == "analyst"


def test_accept_handoff():
    handoff = make_handoff()

    accepted = accept_handoff(
        handoff,
        receiver="analyst",
    )

    assert accepted.status == "accepted"

    # 原始对象不应该被修改
    assert handoff.status == "pending"


def test_wrong_receiver():
    handoff = make_handoff()

    with pytest.raises(HandoffError):
        accept_handoff(
            handoff,
            receiver="reviewer",
        )


def test_duplicate_accept():
    handoff = make_handoff()

    accepted = accept_handoff(
        handoff,
        receiver="analyst",
    )

    with pytest.raises(HandoffError):
        accept_handoff(
            accepted,
            receiver="analyst",
        )


def test_invalid_handoff_route():
    with pytest.raises(HandoffError):
        create_handoff(
            task_id="task-001",
            from_agent="researcher",
            to_agent="reviewer",
            payload={"data": "test"},
        )


def test_reject_handoff():
    handoff = make_handoff()

    rejected = reject_handoff(
        handoff,
        receiver="analyst",
    )

    assert rejected.status == "rejected"
