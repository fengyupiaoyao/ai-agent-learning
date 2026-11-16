def planner_node(state):
    goal = state["goal"]

    tasks = [
        {
            "id": "task_1",
            "description": f"收集 {goal} 的基础资料",
            "status": "pending",
            "result": "",
            "error": "",
            "attempts": 0
        },
        {
            "id": "task_2",
            "description": f"分析 {goal} 的核心技术",
            "status": "pending",
            "result": "",
            "error": "",
            "attempts": 0
        },
        {
            "id": "task_3",
            "description": f"总结 {goal} 的优缺点",
            "status": "pending",
            "result": "",
            "error": "",
            "attempts": 0
        },
        {
            "id": "task_4",
            "description": f"生成 {goal} 的最终报告",
            "status": "pending",
            "result": "",
            "error": "",
            "attempts": 0
        }
    ]

    return {
        "tasks": tasks,
        "current_index": 0,
        "status": "planning"
    }
