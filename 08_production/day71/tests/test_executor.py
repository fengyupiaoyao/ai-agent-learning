from app.executor import executor_node


def test_executor():

    state = {
        "current_index": 0,
        "tasks": [
            {
                "id": "task_1",
                "description": "测试任务",
                "status": "pending",
                "result": "",
                "error": "",
                "attempts": 0
            }
        ],
        "fail_task_id": ""
    }

    result = executor_node(state)

    assert result["status"] == "executing"
    assert result["current_result"]
