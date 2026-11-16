from app.models import Task, TaskResult


def execute_one(task: Task) -> str:
    """
    模拟任务执行。
    后续可以替换成 LLM、工具调用或其他 Agent。
    """

    if "FAIL" in task.description:
        raise RuntimeError("模型任务执行失败")

    return f"已完成: {task.description}"


def execute_tasks(
    tasks: list[Task],
    execution_order: list[str]
) -> list[TaskResult]:
    task_map = {
        task.task_id: task
        for task in tasks
    }

    results: dict[str, TaskResult] = {}

    for task_id in execution_order:
        task = task_map[task_id]

        dependency_results = [
            results.get(dep)
            for dep in task.depends_on
        ]

        blocked = any(
            result is None or result.status != "success"
            for result in dependency_results
        )

        if blocked:
            results[task_id] = TaskResult(
                task_id=task_id,
                status="blocked",
                error="前置任务未全部成功"
            )
            continue

        try:
            output = execute_one(task)

            results[task_id] = TaskResult(
                task_id=task_id,
                status="success",
                output=output
            )
        except Exception as e:
            results[task_id] = TaskResult(
                task_id=task_id,
                status="failed",
                error=str(e)
            )
    return [
        results[task_id]
        for task_id in execution_order
    ]
