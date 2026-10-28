import pytest

from evals.runner import evaluate_answer


@pytest.mark.parametrize(
    "case, answer, expected_pass",
    [
        (
            {
                "id": "test-1",
                "expected_keywords": ["协议", "工具"],
            },
            "MCP 是连接 AI 应用与工具的协议。",
            True,
        ),
        (
            {
                "id": "test-2",
                "expected_keywords": ["协议", "工具"],
            },
            "MCP 可以连接外部系统。",
            False,
        ),
        (
            {
                "id": "test-3",
                "expected_keywords": ["协议"],
            },
            "",
            False,
        ),
    ],
)
def test_evaluate_answer(case, answer, expected_pass):
    result = evaluate_answer(case, answer)
    assert result.passed is expected_pass
