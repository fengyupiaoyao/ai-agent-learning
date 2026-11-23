def evaluate_result(result: dict) -> dict:
    checks = {
        "has_plan": bool(result.get("plan")),
        "has_status": bool(result.get("status")),
        "has_results": bool(result.get("results")),
    }

    score = sum(checks.values()) / len(checks)

    return {
        "score": score,
        "checks": checks,
        "passed": all(checks.values()),
    }
