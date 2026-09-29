from langchain_core.documents import Document

documents = [

    Document(
        page_content="""
        Agent Memory 用于保存 Agent 执行任务过程中
        需要使用的信息，可以帮助 Agent 维护上下文。
        """,
        metadata={
            "topic": "memory",
            "department": "engineering"
        }
    ),

    Document(
        page_content="""
        Tool Calling 允许模型选择并调用外部工具，
        工具可以是 API、数据库或 Python 函数。
        """,
        metadata={
            "topic": "tool",
            "department": "engineering"
        }
    ),

    Document(
        page_content="""
        RAG 通过检索外部知识，再让 LLM
        根据这些知识生成回答。
        """,
        metadata={
            "topic": "rag",
            "department": "engineering"
        }
    ),

    Document(
        page_content="""
        公司员工每年有一定数量的带薪休假，
        具体规则请参考 HR 政策。
        """,
        metadata={
            "topic": "hr",
            "department": "human_resources"
        }
    ),

    Document(
        page_content="""
        员工入职以后需要完成公司的培训流程，
        包括安全培训和公司制度培训。
        """,
        metadata={
            "topic": "hr",
            "department": "human_resources"
        }
    ),
]
