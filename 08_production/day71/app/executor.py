def executor_node(state):
    index = state["current_index"]

    tasks = state["tasks"]

    if index >= len(tasks):
        return {
            "status": "completed"
        }

    task = tasks[index]

    if (
        task["id"] == state["fail_task_id"]
        and task["attempts"] == 0
    ):
        task["attempts"] += 1
        task["status"] = "failed"
        task["error"] = "模拟工具调用失败"

        return {
            "tasks": tasks,
            "current_result": "",
            "current_error": "模拟工具调用失败",
            "status": "failed"
        }

    task["attempts"] += 1

    description = task["description"]

    result = f"已完成任务:{description}"

    task["status"] = "completed"
    task["result"] = result

    return {
        "tasks": tasks,
        "current_result": result,
        "current_error": "",
        "status": "executing"
    }
