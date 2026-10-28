from dataclasses import dataclass
from typing import Any, Callable


@dataclass
class EvalResult:
    case_id: str
    passed: bool
    score: float
    reason: str


def evaluate_keywords(
    case: dict[str, Any],
    answer: str,
) -> EvalResult:
    expected = case["expected_keywords"]

    matched = [
        keyword for keyword in expected if keyword in answer
    ]

    score = len(matched) / len(expected) if expected else 1.0
    passed = score == 1.0

    return EvalResult(
        case_id=case["id"],
        passed=passed,
        score=score,
        reason=f"Matched {matched} out of {expected}"
    )


def evaluate_answer(
    case: dict[str, Any],
    answer: str,
) -> EvalResult:
    if not answer.strip():
        return EvalResult(
            case_id=case["id"],
            passed=False,
            score=0.0,
            reason="Answer is empty"
        )
    return evaluate_keywords(case, answer)
