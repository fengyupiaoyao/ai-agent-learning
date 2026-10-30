from datetime import datetime, timedelta

import pytest

from app.context_compressor import (
    ContextBudgetExceeded,
    ContextCompressor,
    ContextItem,
)


def create_item(
    item_id,
    category,
    content,
    days_ago=0,
):
    return ContextItem(
        item_id=item_id,
        category=category,
        content=content,
        created_at=datetime.now()
        - timedelta(days=days_ago),
    )


def test_mandatory_information_is_preserved():

    items = [
        create_item(
            "1",
            "goal",
            "Build a Research Agent",
        ),
        create_item(
            "2",
            "constraint",
            "Must use Python",
        ),
        create_item(
            "3",
            "noise",
            "Unrelated conversation",
        ),
    ]

    result = ContextCompressor().compress(
        items,
        budget=100,
    )

    categories = {
        item.category for item in result.selected
    }

    assert "goal" in categories
    assert "constraint" in categories


def test_high_priority_information_first():

    items = [
        create_item(
            "1",
            "noise",
            "A" * 80,
        ),
        create_item(
            "2",
            "fact",
            "Important fact",
        ),
    ]

    result = ContextCompressor().compress(
        items,
        budget=10,
    )

    assert any(
        item.item_id == "2"
        for item in result.selected
    )


def test_deduplicate():

    items = [
        create_item("1", "fact", "Python is required"),
        create_item("2", "fact", "Python is required"),
    ]

    result = ContextCompressor().compress(
        items,
        budget=100,
    )

    assert len(result.selected) == 1


def test_budget_is_not_exceeded():

    items = [
        create_item("1", "fact", "Important fact"),
        create_item("2", "recent", "Recent message"),
    ]

    result = ContextCompressor().compress(
        items,
        budget=5,
    )

    assert result.estimated_tokens <= 5


def test_mandatory_context_over_budget():

    items = [
        create_item(
            "1",
            "goal",
            "A" * 100,
        ),
    ]

    with pytest.raises(ContextBudgetExceeded):
        ContextCompressor().compress(
            items,
            budget=2,
        )
