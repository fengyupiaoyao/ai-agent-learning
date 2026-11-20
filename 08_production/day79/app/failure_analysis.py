def analyze_failure(case: dict) -> dict:
    scores = case["scores"]

    failures = []

    if scores["correctness"] < 1.0:
        failures.append({
            "type": "generation_failure",
            "reason": "Answer does not cover all expected keywords."
        })

    if scores["tool_usage"] < 1.0:
        failures.append({
            "type": "tool_selection_failure",
            "reason": "Actual tool calls differ from expected tools."
        })

    if scores["safety"] < 1.0:
        failures.append({
            "type": "safety_failure",
            "reason": "Agent violated the expected safety policy."
        })

    if scores["completion"] < 1.0:
        failures.append({
            "type": "execution_failure",
            "reason": "Task did not reach the expected state."
        })

    return {
        "id": case["id"],
        "failures": failures
    }


def analyze_report(report: dict) -> list:
    analysis = []

    for case in report["results"]:
        if not case["passed"]:
            analysis.append(analyze_failure(case))

    return analysis
