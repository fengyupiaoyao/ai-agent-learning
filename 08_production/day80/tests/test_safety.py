from app.safety import check_tool_safety


def test_delete_file_requires_approval():
    result = check_tool_safety("delete_file")

    assert result["allowed"] is False
    assert result["requires_approval"] is True


def test_search_tool_can_run():
    result = check_tool_safety("search_docs")

    assert result["allowed"] is True
    assert result["requires_approval"] is False
