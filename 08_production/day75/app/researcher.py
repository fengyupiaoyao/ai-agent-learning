from app.state import ResearchItem

KNOWLEDGE_BASE = {
    "LangChain": [
        {
            "key": "main_capability",
            "value": "提供构建 LLM 应用的组件和集成能力",
            "source": "langchain_docs",
            "confidence": 0.95,
        },
        {
            "key": "application",
            "value": "适合构建包含模型、Prompt 和工具调用的应用",
            "source": "langchain_docs",
            "confidence": 0.90,
        },
    ],
    "LangGraph": [
        {
            "key": "main_capability",
            "value": "提供基于图结构的 Agent 工作流编排能力",
            "source": "langgraph_docs",
            "confidence": 0.96,
        },
        {
            "key": "application",
            "value": "适合需要状态管理和循环控制的 Agent 工作流",
            "source": "langgraph_docs",
            "confidence": 0.93,
        },
    ],
    "适用场景": [
        {
            "key": "main_capability",
            "value": "提供基于图结构的 Agent 工作流编排能力",
            "source": "architecture_notes",
            "confidence": 0.88,
        },
        {
            "key": "comparison",
            "value": "应根据工作流复杂度和控制需求选择框架",
            "source": "architecture_notes",
            "confidence": 0.90,
        },
    ],
}


def research_worker(state: dict) -> dict:
    """每次调用只负责研究一个主题。"""
    topic = state["topic"]

    records = KNOWLEDGE_BASE.get(topic, [])

    results: list[ResearchItem] = [
        {
            "topic": topic,
            **record,
        }
        for record in records
    ]

    print(f"[Researcher] 完成主题：{topic}")

    return {
        "results": results
    }
