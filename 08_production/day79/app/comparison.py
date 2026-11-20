def compare_reports(
    v1_report: dict,
    v2_report: dict,
) -> dict:
    v1 = v1_report["summary"]
    v2 = v2_report["summary"]

    score_diff = round(
        v2["average_score"] - v1["average_score"],
        3
    )

    return {
        "baseline": v1["version"],
        "candidate": v2["version"],

        "v1_average_score": v1["average_score"],
        "v2_average_score": v2["average_score"],

        "score_difference": score_diff,

        "v1_passed": v1["passed"],
        "v2_passed": v2["passed"],

        "v1_failed": v1["failed"],
        "v2_failed": v2["failed"],

        "recommendation": (
            "Review required"
            if score_diff < 0
            else "Check regression and safety gates"
        )
    }
