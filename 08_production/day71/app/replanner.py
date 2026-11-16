def replanner_node(state):
    count = state["replan_count"]

    if count >= state["max_replans"]:
        return {
            "status": "failed"
        }

    tasks = state["tasks"]

    index = state["current_index"]

    tasks[index]["description"] += "（使用备用方案）"

    tasks[index]["status"] = "pending"
    tasks[index]["error"] = ""

    return {
        "tasks": tasks,
        "replan_count": count + 1,
        "current_error": "",
        "status": "replanning"
    }
