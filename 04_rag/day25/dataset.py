from dataclasses import dataclass


@dataclass
class EvaluationCase:
    question: str
    expected_answer: str
    expected_source: str


dataset = [
    EvaluationCase(
        question="Agent 是什么？",
        expected_source="agent_intro",
        expected_answer=(
            "AI Agent 是能够感知环境、进行推理、"
            "调用工具并完成任务的智能系统。"
        ),
    ),

    EvaluationCase(
        question="Agent 如何保存长期记忆？",
        expected_source="agent_memory",
        expected_answer=(
            "Agent Memory 用于保存 Agent 在执行任务过程中"
            "需要使用的信息。"
        ),
    ),

    EvaluationCase(
        question="Tool Calling 是什么？",
        expected_source="tool_calling",
        expected_answer=(
            "Tool Calling 允许 LLM 根据任务需求选择并调用外部工具。"
        ),
    ),

    EvaluationCase(
        question="什么是 RAG？",
        expected_source="rag_intro",
        expected_answer=(
            "RAG 通过先检索相关知识，再将检索结果提供给 LLM，"
            "从而让模型利用外部知识回答问题。"
        ),
    ),
]
