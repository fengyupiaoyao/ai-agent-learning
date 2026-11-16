from app.models import Task
from app.executor import execute_tasks


def test_failed_task_blocks_downstream():
    tasks = [
        Task(
            task_id="T1",
            description="FAIL 模拟失败",
        ),
        Task(
            task_id="T2",
            description="依赖 T1",
            depends_on=["T1"],
        ),
        Task(
            task_id="T3",
            description="依赖 T2",
            depends_on=["T2"],
        ),
    ]

    results = execute_tasks(
        tasks,
        ["T1", "T2", "T3"],
    )

    result_map = {
        result.task_id: result
        for result in results
    }

    assert result_map["T1"].status == "failed"
    assert result_map["T2"].status == "blocked"
    assert result_map["T3"].status == "blocked"


def test_successful_execution():
    tasks = [
        Task(task_id="T1", description="task 1"),
        Task(
            task_id="T2",
            description="task 2",
            depends_on=["T1"],
        ),
    ]

    results = execute_tasks(tasks, ["T1", "T2"])

    assert all(
        result.status == "success"
        for result in results
    )
