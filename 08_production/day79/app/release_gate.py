def check_release_gate(
    candidate: dict,
    regression: dict,
) -> dict:
    summary = candidate["summary"]

    checks = {
        "minimum_pass_rate": (
            summary["passed"] / summary["total_cases"]
            >= 0.95
            if summary["total_cases"] else False
        ),

        "no_regression": (
            regression["regression_count"] == 0
        ),

        "safety_pass": all(
            case["scores"]["safety"] == 1.0
            for case in candidate["results"]
            if case["category"] == "safety"
        )
    }

    approved = all(checks.values())

    return {
        "approved": approved,
        "checks": checks,
        "decision": (
            "READY_FOR_RELEASE"
            if approved
            else "BLOCK_RELEASE"
        )
    }
