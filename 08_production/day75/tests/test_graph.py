from app.graph import graph


def test_parallel_research_graph():
    result = graph.invoke({
        "goal": "研究 Agent 框架",
        "topics": [
            "LangChain",
            "LangGraph",
            "适用场景",
        ],
        "results": [],
        "merged": {},
    })

    merged = result["merged"]

    assert merged["total_raw_results"] == 6
    assert merged["total_merged_items"] == 5

    assert len(merged["conflicts"]) >= 1

    assert len(result["results"]) == 6
