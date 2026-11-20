from app.evaluators import (
    evaluate_correctness,
    evaluate_tool_usage,
    evaluate_safety,
    evaluate_completion,
)


def test_correctness():

    score = evaluate_correctness(
        "Checkpoint saves state and supports resume",
        ["checkpoint", "state", "resume"]
    )

    assert score == 1.0


def test_incorrect_answer():

    score = evaluate_correctness(
        "This is an unrelated answer",
        ["checkpoint", "state"]
    )

    assert score == 0.0


def test_tool_usage():

    score = evaluate_tool_usage(
        ["search_docs"],
        ["search_docs"]
    )

    assert score == 1.0


def test_wrong_tool():

    score = evaluate_tool_usage(
        ["delete_file"],
        ["search_docs"]
    )

    assert score == 0.0


def test_safety():

    assert evaluate_safety(True, True) == 1.0

    assert evaluate_safety(False, True) == 0.0


def test_approval_completion():

    score = evaluate_completion(
        "waiting_approval",
        "safety"
    )

    assert score == 1.0


def test_tool_error():

    score = evaluate_completion(
        "failed",
        "tool_error"
    )

    assert score == 1.0
