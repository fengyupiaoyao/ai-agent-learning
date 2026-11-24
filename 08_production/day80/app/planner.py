def create_plan(user_input: str) -> list[str]:
    """
    根据用户输入生成任务计划。
    当前先用规则模拟，后续可以替换成 LLM Planner。
    """
    text = user_input.lower()

    if "删除" in user_input or "delete" in text:
        return [
            "分析删除请求",
            "检查操作风险",
            "等待人工审批",
            "执行删除操作",
            "返回执行结果",
        ]

    if "分析" in user_input or "analyze" in text:
        return [
            "收集相关资料",
            "分析资料内容",
            "生成分析报告",
            "检查结果质量",
        ]

    return [
        "理解用户请求",
        "查询相关资料",
        "整理结果",
        "返回最终答案",
    ]
