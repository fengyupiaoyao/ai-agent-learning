from langchain_core.documents import Document

documents = [
    Document(
        page_content="""
        AI Agent 是能够感知环境、进行推理、调用工具并完成任务的智能系统。
        Agent 通常由 LLM、Tools、Memory 和执行逻辑组成。
        """,
        metadata={
            "topic": "agent",
            "source": "agent_intro"
        }
    ),

    Document(
        page_content="""
        Tool Calling 允许 LLM 根据任务需求选择并调用外部工具。
        Tool 可以是搜索工具、数据库工具、API 或 Python 函数。
        """,
        metadata={
            "topic": "tool",
            "source": "tool_calling"
        }
    ),

    Document(
        page_content="""
        Agent Memory 用于保存 Agent 在执行任务过程中需要使用的信息。
        Memory 可以帮助 Agent 维护对话上下文，也可以用于长期信息存储。
        """,
        metadata={
            "topic": "memory",
            "source": "agent_memory"
        }
    ),

    Document(
        page_content="""
        RAG，即 Retrieval Augmented Generation，
        通过先检索相关知识，再将检索结果提供给 LLM，
        从而让模型能够利用外部知识回答问题。
        """,
        metadata={
            "topic": "rag",
            "source": "rag_intro"
        }
    ),

    Document(
        page_content="""
        LangChain 是用于构建基于大语言模型应用的开发框架。
        它提供模型、Prompt、Tools、Retrievers、Agents 等组件。
        """,
        metadata={
            "topic": "langchain",
            "source": "langchain_intro"
        }
    ),

    Document(
        page_content="""
        LangGraph 用于构建具有状态、循环、条件路由和多步骤执行能力的 Agent。
        它可以将 Agent 拆分为多个 Node，并通过 Edge 控制执行流程。
        """,
        metadata={
            "topic": "langgraph",
            "source": "langgraph_intro"
        }
    ),
]
