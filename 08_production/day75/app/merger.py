from collections import defaultdict


def merge_results(state: dict) -> dict:
    results = state["results"]

    grouped = defaultdict(list)

    for item in results:
        grouped[item["key"]].append(item)

    merged_items = []
    conflicts = []

    for key, items in grouped.items():
        value_groups = defaultdict(list)

        for item in items:
            value_groups[item["value"]].append(item)

        if len(value_groups) > 1:
            conflicts.append({
                "key": key,
                "candidates": [
                    {
                        "value": value,
                        "sources": sorted({
                            item["source"] for item in group
                        }),
                    }
                    for value, group in value_groups.items()
                ],
            })

        for value, group in value_groups.items():
            merged_items.append({
                "key": key,
                "value": value,
                "sources": sorted({
                    item["source"] for item in group
                }),
                "topics": sorted({
                    item["topic"] for item in group
                }),
                "confidence": max(
                    item["confidence"] for item in group
                ),
                "has_conflict": len(value_groups) > 1,
            })

    return {
        "merged": {
            "goal": state["goal"],
            "items": merged_items,
            "conflicts": conflicts,
            "total_raw_results": len(results),
            "total_merged_items": len(merged_items),
        }
    }
