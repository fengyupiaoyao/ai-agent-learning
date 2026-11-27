from typing import Literal

from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    ToolMessage,
)

from langgraph.graph import (
    StateGraph,
    START,
    END,
)

from langgraph.prebuilt import ToolNode

from app.agents.state import ResearchState
from app.agents.planner import ResearchPlan
from app.tools.research_tools import build_research_tools

import os
from dotenv import load_dotenv
load_dotenv()


class ResearchGraph:
    def __init__(
        self,
        knowledge_base_service,
        user_id: str,
    ):
        self.llm = ChatOpenAI(
            model="qwen3.8-max",
            api_key=os.environ["OPENAI_API_KEY"],
            base_url="https://ws-wopagvlf3afu5baf.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            temperature=0,
        )

        self.knowledge_base_service = knowledge_base_service

        self.user_id = user_id

        self.tools = build_research_tools(
            knowledge_base_service,
            user_id,
        )

        self.tools_by_name = {
            tool.name: tool
            for tool in self.tools
        }

        self.workflow = self._build_graph()

    def _build_graph(self):
        graph = StateGraph(ResearchState)

        graph.add_node(
            "planner",
            self.plan_research,
        )

        graph.add_node(
            "prepare_step",
            self.prepare_step,
        )

        graph.add_node(
            "call_tool_model",
            self.call_tool_model,
        )

        graph.add_node(
            "tools",
            ToolNode(self.tools),
        )

        graph.add_node(
            "collect_results",
            self.collect_results,
        )

        graph.add_edge(
            START,
            "planner",
        )

        graph.add_edge(
            "planner",
            "prepare_step",
        )

        graph.add_edge(
            "prepare_step",
            "call_tool_model",
        )

        graph.add_conditional_edges(
            "call_tool_model",
            self.route_tool_call,
            {
                "tools": "tools",
                "collect": "collect_results",
            },
        )

        graph.add_edge(
            "tools",
            "collect_results",
        )

        graph.add_conditional_edges(
            "collect_results",
            self.should_continue,
            {
                "continue": "prepare_step",
                "end": END,
            },
        )

        return graph.compile()

    # ---------------------------------
    # Node 1: Research Planning
    # ---------------------------------

    def plan_research(
        self,
        state: ResearchState,
    ):

        planner = self.llm.with_structured_output(
            ResearchPlan
        )

        prompt = f"""
你是一个专业的技术研究规划 Agent。

请分析用户的研究目标，并生成有序研究计划。

用户问题：
{state["question"]}

最多生成 {state.get("max_steps", 5)} 个步骤。

要求：

1. 将复杂问题拆分为独立研究任务。
2. 每个任务必须有明确目标。
3. 每个任务必须选择一个工具。
4. 内部资料使用 knowledge_search。
5. 外部公开资料使用 web_search。
6. query 必须是可以直接执行的检索问题。
7. 不要生成重复的研究步骤。
8. 优先完成基础概念，再研究实现机制和实际应用。
"""

        plan = planner.invoke(prompt)

        steps = [
            step.model_dump()
            for step in plan.steps[
                :state.get("max_steps", 5)
            ]
        ]

        return {
            "research_plan": steps,
            "current_step": 0,
            "status": "running",
        }

    # ---------------------------------
    # Node 2: Prepare Current Step
    # ---------------------------------

    def prepare_step(
        self,
        state: ResearchState,
    ):

        index = state["current_step"]

        step = state["research_plan"][index]

        message = HumanMessage(
            content=f"""
现在执行研究计划中的一个步骤。

研究目标：
{state["question"]}

当前步骤：
{step["task"]}

必须使用的工具：
{step["tool"]}

工具查询内容：
{step["query"]}

请调用指定工具完成任务。
不要调用其他工具。
"""
        )

        return {
            "messages": [message]
        }

    # ---------------------------------
    # Node 3: Model Tool Calling
    # ---------------------------------

    def call_tool_model(
        self,
        state: ResearchState,
    ):

        index = state["current_step"]

        step = state["research_plan"][index]

        selected_tool = self.tools_by_name[
            step["tool"]
        ]

        llm_with_tool = self.llm.bind_tools(
            [selected_tool],
            tool_choice=selected_tool.name,
        )

        response = llm_with_tool.invoke(
            state["messages"]
        )

        return {
            "messages": [response]
        }

    # ---------------------------------
    # Conditional Routing
    # ---------------------------------

    def route_tool_call(
        self,
        state: ResearchState,
    ) -> Literal["tools", "collect"]:

        last_message = state["messages"][-1]

        if (
            isinstance(last_message, AIMessage)
            and last_message.tool_calls
        ):
            return "tools"

        return "collect"

    # ---------------------------------
    # Node 4: Collect Results
    # ---------------------------------

    def collect_results(
        self,
        state: ResearchState,
    ):

        index = state["current_step"]

        step = state["research_plan"][index]

        tool_messages = [
            message
            for message in state["messages"]
            if isinstance(message, ToolMessage)
        ]

        if tool_messages:

            result = str(
                tool_messages[-1].content
            )

        else:

            last_message = state["messages"][-1]

            result = str(
                getattr(
                    last_message,
                    "content",
                    "工具没有返回结果",
                )
            )

        return {
            "research_results": [
                {
                    "step_id": step["step_id"],
                    "task": step["task"],
                    "tool": step["tool"],
                    "query": step["query"],
                    "result": result,
                }
            ],
            "current_step": index + 1,
        }

    # ---------------------------------
    # Conditional Routing
    # ---------------------------------

    def should_continue(
        self,
        state: ResearchState,
    ) -> Literal["continue", "end"]:

        if (
            state["current_step"]
            < len(state["research_plan"])
        ):
            return "continue"

        return "end"

    def invoke(
        self,
        question: str,
        max_steps: int = 5,
    ):

        initial_state: ResearchState = {
            "question": question,
            "user_id": self.user_id,
            "max_steps": max_steps,
            "research_plan": [],
            "current_step": 0,
            "messages": [],
            "research_results": [],
            "status": "pending",
        }

        return self.workflow.invoke(
            initial_state,
            config={
                "recursion_limit": 50,
            },
        )
