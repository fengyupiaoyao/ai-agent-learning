from app.contracts import (
    Finding,
    ResearchOutput,
    AnalysisOutput,
    ReviewOutput,
)

from app.tools import call_tool


def research_agent(goal: str) -> ResearchOutput:
    raw_findings = call_tool("researcher", "search_docs", query=goal)

    findings = [
        Finding(**item)
        for item in raw_findings
    ]

    return ResearchOutput(
        topic=goal,
        findings=findings,
        status="completed",
    )


def analysis_agent(
    research: ResearchOutput,
) -> AnalysisOutput:
    raw = call_tool("analyst", "analyze_data", findings=[
        item.model_dump()
        for item in research.findings
    ])

    return AnalysisOutput(
        topic=research.topic,
        advantages=raw["advantages"],
        disadvantages=raw["disadvantages"],
        conclusion=raw["conclusion"],
    )


def review_agent(
    analysis: AnalysisOutput,
) -> ReviewOutput:
    raw = call_tool("reviewer", "validate_report",
                    analysis=analysis.model_dump())

    return ReviewOutput(**raw)
