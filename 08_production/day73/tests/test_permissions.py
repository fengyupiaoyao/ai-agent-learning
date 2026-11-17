import pytest

from app.tools import (
    call_tool,
    PermissionDenied,
)


def test_researcher_can_search():
    result = call_tool(
        "researcher",
        "search_docs",
        query="LangGraph",
    )

    assert len(result) > 0


def test_researcher_cannot_analyze():
    with pytest.raises(PermissionDenied):
        call_tool(
            "researcher",
            "analyze_data",
            findings=[],
        )


def test_analyst_cannot_search():
    with pytest.raises(PermissionDenied):
        call_tool(
            "analyst",
            "search_docs",
            query="LangGraph",
        )


def test_unknown_role():
    with pytest.raises(PermissionDenied):
        call_tool(
            "unknown",
            "search_docs",
            query="test",
        )
