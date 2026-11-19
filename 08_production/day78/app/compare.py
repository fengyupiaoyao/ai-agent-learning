def compare_versions(
    v1_results: list[dict],
    v2_results: list[dict]
):

    print("===== Version Comparison =====")

    for v1, v2 in zip(v1_results, v2_results):

        print(f"\nTest Case: {v1['id']}")

        print(
            "V1:",
            v1["total_score"]
        )

        print(
            "V2:",
            v2["total_score"]
        )

        improvement = (
            v2["total_score"]
            - v1["total_score"]
        )

        print(
            "Improvement:",
            round(improvement, 3)
        )

    v1_avg = sum(
        x["total_score"]
        for x in v1_results
    ) / len(v1_results)

    v2_avg = sum(
        x["total_score"]
        for x in v2_results
    ) / len(v2_results)

    print("\nV1 Average:", round(v1_avg, 3))
    print("V2 Average:", round(v2_avg, 3))

    print(
        "Overall Improvement:",
        round(v2_avg - v1_avg, 3)
    )
