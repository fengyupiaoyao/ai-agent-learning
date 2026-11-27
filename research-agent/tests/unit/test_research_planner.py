import pytest

from pydantic import ValidationError

from app.agents.planner import (
    ResearchPlan,
    ResearchStep,
)

from app.tools.research_tools import (
    build_research_tools,
)


def test_research_step():

    step = ResearchStep(
        step_id="step_1",
        task="研究 Checkpoint 基础概念",
        tool="knowledge_search",
        query="LangGraph Checkpoint 是什么",
    )

    assert step.step_id == "step_1"

    assert step.tool == "knowledge_search"


def test_invalid_tool():

    with pytest.raises(ValidationError):

        ResearchStep(
            step_id="step_1",
            task="研究 Checkpoint",
            tool="unknown_tool",
            query="Checkpoint",
        )


def test_research_plan():

    plan = ResearchPlan(
        goal="研究 LangGraph",
        steps=[
            ResearchStep(
                step_id="step_1",
                task="研究 StateGraph",
                tool="knowledge_search",
                query="StateGraph 的工作机制",
            )
        ],
    )

    assert len(plan.steps) == 1


def test_empty_research_plan():

    with pytest.raises(ValidationError):

        ResearchPlan(
            goal="研究 LangGraph",
            steps=[],
        )


class FakeKnowledgeBase:

    def search(
        self,
        query,
        user_id,
        k=5,
    ):

        assert user_id == "user_001"

        return []


class FakeWebSearch:

    def invoke(self, args):

        return {
            "query": args["query"],
            "results": [
                {"title": "Test Result"}
            ],
        }


def test_knowledge_search_tool():

    tools = build_research_tools(
        knowledge_base_service=FakeKnowledgeBase(),
        user_id="user_001",
        web_search_backend=FakeWebSearch(),
    )

    knowledge_tool = next(
        tool for tool in tools
        if tool.name == "knowledge_search"
    )

    result = knowledge_tool.invoke({
        "query": "LangGraph Checkpoint"
    })

    assert "没有找到" in result


def test_web_search_tool():

    tools = build_research_tools(
        knowledge_base_service=FakeKnowledgeBase(),
        user_id="user_001",
        web_search_backend=FakeWebSearch(),
    )

    web_tool = next(
        tool for tool in tools
        if tool.name == "web_search"
    )

    result = web_tool.invoke({
        "query": "LangGraph"
    })

    assert "Test Result" in result
