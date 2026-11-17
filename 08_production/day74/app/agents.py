from app.contracts import (
    ResearchResult,
    AnalysisResult,
    ReviewResult,
)


def researcher_agent(goal: str) -> ResearchResult:
    """模拟 Researcher 搜集资料。"""

    return ResearchResult(
        topic=goal,
        findings=[
            {
                "title": "LangChain",
                "content": "提供 LLM 应用和工具调用相关抽象",
                "source": "official_docs",
            },
            {
                "title": "LangGraph",
                "content": "支持有状态的 Agent 工作流编排",
                "source": "official_docs",
            },
        ],
        conclusion="已收集两个框架的基础资料",
    )


def analyst_agent(
    research: ResearchResult,
) -> AnalysisResult:
    """模拟 Analyst 分析研究结果。"""

    if not research.findings:
        raise ValueError("没有可分析的研究资料")

    return AnalysisResult(
        topic=research.topic,
        advantages=[
            "LangChain 提供丰富的 LLM 应用开发抽象",
            "LangGraph 适合复杂、有状态的工作流",
        ],
        disadvantages=[
            "需要根据实际项目选择合适的技术抽象",
        ],
        conclusion=(
            "简单 LLM 应用可以考虑 LangChain，"
            "复杂流程可以考虑 LangGraph"
        ),
    )


def reviewer_agent(
    analysis: AnalysisResult,
) -> ReviewResult:
    """模拟 Reviewer 检查分析结果。"""

    complete = (
        bool(analysis.advantages)
        and bool(analysis.disadvantages)
        and bool(analysis.conclusion)
    )

    return ReviewResult(
        approved=complete,
        score=90 if complete else 40,
        feedback=(
            "分析内容完整"
            if complete
            else "分析内容不完整，需要补充"
        ),
    )
