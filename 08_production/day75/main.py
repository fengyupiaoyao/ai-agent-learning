import json

from app.graph import graph


def main():
    initial_state = {
        "goal": "研究 LangChain 和 LangGraph 的能力及适用场景",
        "topics": [
            "LangChain",
            "LangGraph",
            "适用场景",
        ],
        "results": [],
        "merged": {},
    }

    result = graph.invoke(initial_state)

    print("\n========== 合并结果 ==========")

    print(
        json.dumps(
            result["merged"],
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
