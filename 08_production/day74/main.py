from app.graph import graph

result = graph.invoke({
    "task_id": "research-task-001",
    "goal": "研究 LangChain 和 LangGraph 的区别",

    "research": None,
    "analysis": None,
    "review": None,

    "current_handoff": None,
    "handoff_log": [],

    "status": "started",
})

print("最终状态：", result["status"])

print("\n分析结果：")
print(result["analysis"].model_dump())

print("\n评审结果：")
print(result["review"].model_dump())

print("\n交接记录：")

for item in result["handoff_log"]:
    print({
        "handoff_id": item["handoff_id"],
        "from": item["from_agent"],
        "to": item["to_agent"],
        "status": item["status"],
    })
