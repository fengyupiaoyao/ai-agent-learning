from collections import deque
from app.models import Task


class DependencyError(Exception):
    pass


def topological_sort(tasks: list[Task]) -> list[str]:
    task_map = {
        task.task_id: task
        for task in tasks
    }

    if len(task_map) != len(tasks):
        raise DependencyError("存在重复的 task_id ")

    in_degree = {
        task.task_id: 0
        for task in tasks
    }

    graph = {
        task.task_id: []
        for task in tasks
    }

    for task in tasks:
        for dependency in task.depends_on:
            if dependency not in task_map:
                raise DependencyError(
                    f"任务 {task.task_id} 依赖的 task_id {dependency} 不存在"
                )

            if dependency == task.task_id:
                raise DependencyError(
                    f"任务 {task.task_id} 依赖于自己"
                )

            graph[dependency].append(task.task_id)
            in_degree[task.task_id] += 1

    queue = deque(
        task_id
        for task_id, degree in in_degree.items()
        if degree == 0
    )

    order = []

    while queue:
        current = queue.popleft()
        order.append(current)

        for next_task in graph[current]:
            in_degree[next_task] -= 1

            if in_degree[next_task] == 0:
                queue.append(next_task)

    if len(order) != len(tasks):
        raise DependencyError("存在循环依赖")

    return order
