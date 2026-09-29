from langchain_core.documents import Document


documents = [

    Document(
        page_content=(
            "AI Agent 是能够感知环境、进行推理、"
            "调用工具并完成任务的智能系统。"
        ),
        metadata={
            "source": "agent_intro",
            "topic": "agent",
        },
    ),

    Document(
        page_content=(
            "Tool Calling 允许 LLM 根据任务需求"
            "选择并调用外部工具。"
        ),
        metadata={
            "source": "tool_calling",
            "topic": "tool",
        },
    ),

    Document(
        page_content=(
            "Agent Memory 用于保存 Agent 在执行任务"
            "过程中需要使用的信息。"
        ),
        metadata={
            "source": "agent_memory",
            "topic": "memory",
        },
    ),

    Document(
        page_content=(
            "RAG 通过先检索相关知识，再将检索结果"
            "提供给 LLM，从而让模型利用外部知识回答问题。"
        ),
        metadata={
            "source": "rag_intro",
            "topic": "rag",
        },
    ),
]
