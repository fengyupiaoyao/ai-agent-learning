from app.models import Task
from app.graph import graph

tasks = [
    Task(
        task_id="T1",
        description="搜集 LangChain 资料",
    ),
    Task(
        task_id="T2",
        description="搜集 LangGraph 资料",
    ),
    Task(
        task_id="T3",
        description="比较两个框架",
        depends_on=["T1", "T2"],
    ),
    Task(
        task_id="T4",
        description="整理技术选型建议",
        depends_on=["T3"],
    ),
    Task(
        task_id="T5",
        description="生成最终报告",
        depends_on=["T4"],
    ),
]

result = graph.invoke({
    "tasks": tasks,
    "execution_order": [],
    "results": []
})

print("执行顺序：")
print(result["execution_order"])

print("\n执行结果：")
for item in result["results"]:
    print(item.model_dump())
