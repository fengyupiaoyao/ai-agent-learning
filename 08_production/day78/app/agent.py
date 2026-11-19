def run_agent(task: str) -> dict:
    """
    模拟 Agent 执行任务。
    返回答案、工具调用和安全状态。
    """
    task_lower = task.lower()

    if "删除" in task:
        return {
            "answer": "This operation requires approval.",
            "tool_calls": ["delete_file"],
            "safe": True,
            "status": "waiting_approval"
        }
    if "发送邮件" in task:
        return {
            "answer": "Email sending requires approval.",
            "tool_calls": ["send_email"],
            "safe": True,
            "status": "waiting_approval"
        }

    if "不存在" in task:
        return {
            "answer": "Document not found.",
            "tool_calls": ["search_docs"],
            "safe": True,
            "status": "completed"
        }

    if "搜索" in task and "LangGraph" in task:
        return {
            "answer": "Search error: service unavailable.",
            "tool_calls": ["search_docs"],
            "safe": True,
            "status": "failed"
        }

    if "Checkpoint" in task:
        return {
            "answer": (
                "Checkpoint saves workflow state "
                "and supports resume."
            ),
            "tool_calls": ["search_docs"],
            "safe": True,
            "status": "completed"
        }

    if "SSE" in task:
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

    if "Memory" in task:
        return {
            "answer": (
                "Agent memory stores context "
                "and helps maintain conversation information."
            ),
            "tool_calls": ["search_docs"],
            "safe": True,
            "status": "completed"
        }

    if "asyncio" in task:
        return {
            "answer": (
                "Python asyncio supports async "
                "and asynchronous programming."
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
