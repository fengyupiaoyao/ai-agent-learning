from langchain_core.prompts import ChatPromptTemplate
from llm import model
from rich import print as pprint

prompt = ChatPromptTemplate.from_template("""
你是一个 RAG 检索专家。

针对下面的问题，生成 4 个不同角度的搜索查询。

要求：
- 每个查询表达相同的核心需求
- 使用不同的关键词和表达方式
- 每行一个 Query
- 不要添加编号

原问题：

{question}
""")

chain = prompt | model


def generate_queries(question: str) -> str:
    result = chain.invoke([
        {"question": question}
    ])
    pprint(result.content)
    queries = [
        line.strip()
        for line in result.content.splitlines()
        if line.strip()
    ]
    return queries
