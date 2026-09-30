from langchain_core.prompts import ChatPromptTemplate
from llm import model

prompt = ChatPromptTemplate.from_template("""
你是一个 RAG Query Rewrite 专家。

请将用户的问题改写成更加适合知识库检索的查询。

要求：
1. 保留原始问题的核心含义
2. 补充必要的专业关键词
3. 删除无意义的口语表达
4. 只输出改写后的问题

用户问题：

{question}
""")

rewrite_chain = prompt | model


def rewrite_query(question: str) -> str:
    result = rewrite_chain.invoke({"question": question})
    return result.content
