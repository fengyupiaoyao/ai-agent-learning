from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

text = """
AI Agent 是能够感知环境、进行推理、
调用工具并完成任务的智能系统。

Agent 通常由 LLM、Tools、Memory
以及执行逻辑组成。

Tool Calling 允许 LLM 根据任务需求
选择并调用外部工具。

Memory 用于保存 Agent 执行任务过程中
需要使用的信息。

RAG 通过检索外部知识，
让 LLM 能够利用额外的信息回答问题。
"""

document = Document(
    page_content=text,
    metadata={
        "topic": "AI Agent",
        "source": "example.txt"
    },
)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=0,
)

chunks = text_splitter.split_documents([document])
print(chunks)
