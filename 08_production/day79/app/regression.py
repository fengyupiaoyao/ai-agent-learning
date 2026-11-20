def detect_regressions(
    baseline: dict,
    candidate: dict,
) -> dict:
    baseline_map = {
        item["id"]: item
        for item in baseline["results"]
    }

    condidate_map = {
        item["id"]: item
        for item in candidate["results"]
    }

    regressions = []
    improvements = []
    unchanged = []

    for case_id in baseline_map.keys() & condidate_map.keys():
        old = baseline_map[case_id]
        new = condidate_map[case_id]

        if old["passed"] and not new["passed"]:
            regressions.append({
                "id": case_id,
                "old_score": old["total_score"],
                "new_score": new["total_score"]
            })
        elif not old["passed"] and new["passed"]:
            improvements.append(case_id)
        else:
            unchanged.append(case_id)

    return {
        "regression": regressions,
        "improvements": improvements,
        "unchanged": unchanged,
        "regression_count": len(regressions)
    }
