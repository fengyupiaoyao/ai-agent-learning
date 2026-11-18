from app.merger import merge_results


def test_duplicate_results_merge_sources():
    state = {
        "goal": "test",
        "results": [
            {
                "topic": "A",
                "key": "framework",
                "value": "LangGraph",
                "source": "source_a",
                "confidence": 0.8,
            },
            {
                "topic": "B",
                "key": "framework",
                "value": "LangGraph",
                "source": "source_b",
                "confidence": 0.9,
            },
        ],
    }

    result = merge_results(state)["merged"]

    assert len(result["items"]) == 1

    item = result["items"][0]

    assert item["sources"] == ["source_a", "source_b"]
    assert item["confidence"] == 0.9
    assert item["has_conflict"] is False


def test_conflicting_results_are_preserved():
    state = {
        "goal": "test",
        "results": [
            {
                "topic": "A",
                "key": "database",
                "value": "PostgreSQL",
                "source": "source_a",
                "confidence": 0.9,
            },
            {
                "topic": "B",
                "key": "database",
                "value": "MySQL",
                "source": "source_b",
                "confidence": 0.8,
            },
        ],
    }

    result = merge_results(state)["merged"]

    assert len(result["conflicts"]) == 1
    assert len(result["items"]) == 2

    assert all(
        item["has_conflict"]
        for item in result["items"]
    )
