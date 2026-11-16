def evaluator_node(state):
    if state["current_error"]:
        return {
            "status": "failed"
        }

    tasks = state["tasks"]

    index = state["current_index"]

    task = tasks[index]

    result = state["current_result"]

    if not result:
        task["status"] = "failed"

        return {
            "tasks": tasks,
            "current_error": "任务执行结果为空",
            "status": "failed"
        }

    task["status"] = "completed"

    results = state["results"] + [result]

    return {
        "tasks": tasks,
        "results": results,
        "current_index": index + 1,
        "current_error": "",
        "status": "evaluated"
    }
