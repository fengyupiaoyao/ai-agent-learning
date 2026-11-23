def check_release(
    evaluation_results: list[dict],
    regression_detected: bool,
    safety_passed: bool,
) -> dict:
    if not evaluation_results:
        return {
            "approved": False,
            "reason": "没有评测结果",
        }

    pass_rate = sum(
        item["passed"] for item in evaluation_results
    ) / len(evaluation_results)

    approved = (
        pass_rate >= 0.95
        and not regression_detected
        and safety_passed
    )

    return {
        "approved": approved,
        "pass_rate": pass_rate,
        "regression_detected": regression_detected,
        "safety_passed": safety_passed,
    }
