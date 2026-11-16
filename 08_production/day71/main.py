from app.graph import build_graph


def main():
    graph = build_graph()

    initial_state = {
        "goal": "AI Agent 框架技术研究",

        "tasks": [],

        "current_index": 0,

        "results": [],

        "replan_count": 0,

        "max_replans": 3,

        "current_result": "",

        "current_error": "",

        "status": "pending",

        "fail_task_id": "task_2"
    }

    result = graph.invoke(initial_state)

    print("\n========== Planning Result ==========")

    print("Goal:", result["goal"])

    print("Status:", result["status"])

    print("\nTasks:")

    for task in result["tasks"]:
        print(
            task["id"],
            task["description"],
            task["status"]
        )

    print("\nResults:")

    for item in result["results"]:
        print(item)


if __name__ == "__main__":
    main()
