from app.graph import graph

result = graph.invoke({
    "goal": "研究 LangChain 和 LangGraph 的区别",
    "research": None,
    "analysis": None,
    "review": None,
    "review_round": 0,
    "status": "started",
})

print("最终状态：", result["status"])

print("\n研究资料：")
print(result["research"].model_dump())

print("\n分析结果：")
print(result["analysis"].model_dump())

print("\n评审结果：")
print(result["review"].model_dump())
print("评审轮数：", result["review_round"])
