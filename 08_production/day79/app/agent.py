def run_agent(task: str, version: str = "v1") -> dict:

    task_lower = task.lower()

    # V1：旧版本
    if version == "v1":

        if "删除" in task:
            return {
                "answer": "This operation requires approval.",
                "tool_calls": ["delete_file"],
                "safe": True,
                "status": "waiting_approval"
            }

        if "checkpoint" in task_lower:
            return {
                "answer": (
                    "Checkpoint saves workflow state "
                    "and supports resume."
                ),
                "tool_calls": ["search_docs"],
                "safe": True,
                "status": "completed"
            }

        if "sse" in task_lower:
            return {
                "answer": (
                    "SSE uses a server connection for "
                    "streaming, while WebSocket supports "
                    "bidirectional communication."
                ),
                "tool_calls": ["search_docs"],
                "safe": True,
                "status": "completed"
            }

    # V2：新版本
    if version == "v2":

        if "删除" in task:
            return {
                "answer": "Deleting file now.",
                "tool_calls": ["delete_file"],
                "safe": False,
                "status": "completed"
            }

        if "checkpoint" in task_lower:
            return {
                "answer": (
                    "Checkpoint saves workflow state "
                    "and supports resume."
                ),
                "tool_calls": ["search_docs"],
                "safe": True,
                "status": "completed"
            }

        if "sse" in task_lower:
            return {
                "answer": (
                    "SSE supports server streaming."
                ),
                "tool_calls": ["search_docs"],
                "safe": True,
                "status": "completed"
            }

    return {
        "answer": "I cannot handle this task.",
        "tool_calls": [],
        "safe": True,
        "status": "failed"
    }
