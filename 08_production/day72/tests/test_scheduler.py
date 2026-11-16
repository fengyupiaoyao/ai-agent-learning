import pytest

from app.models import Task
from app.scheduler import (
    topological_sort,
    DependencyError,
)


def test_topological_sort():
    tasks = [
        Task(task_id="T1", description="task 1"),
        Task(task_id="T2", description="task 2"),
        Task(
            task_id="T3",
            description="task 3",
            depends_on=["T1", "T2"],
        ),
        Task(
            task_id="T4",
            description="task 4",
            depends_on=["T3"],
        ),
    ]

    order = topological_sort(tasks)

    assert order.index("T1") < order.index("T3")
    assert order.index("T2") < order.index("T3")
    assert order.index("T3") < order.index("T4")


def test_missing_dependency():
    tasks = [
        Task(
            task_id="T1",
            description="task 1",
            depends_on=["T99"],
        )
    ]

    with pytest.raises(DependencyError):
        topological_sort(tasks)


def test_cycle_dependency():
    tasks = [
        Task(
            task_id="T1",
            description="task 1",
            depends_on=["T2"],
        ),
        Task(
            task_id="T2",
            description="task 2",
            depends_on=["T1"],
        ),
    ]

    with pytest.raises(DependencyError):
        topological_sort(tasks)


def test_duplicate_task_id():
    tasks = [
        Task(task_id="T1", description="task 1"),
        Task(task_id="T1", description="duplicate"),
    ]

    with pytest.raises(DependencyError):
        topological_sort(tasks)
