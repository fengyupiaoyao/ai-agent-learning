from retriever import create_retriever


def print_results(query: str):
    retriever = create_retriever()
    results = retriever.invoke(query)

    print("Query:", query)
    print("=" * 50)

    for i, doc in enumerate(results):
        print(f"Document {i+1}:")
        print(f"  Page Content: {doc.page_content}")
        print(f"  Metadata: {doc.metadata}")
        print("=" * 50)


queries = [
    "Agent 如何使用工具？",
    "什么是 RAG？",
    "LangGraph 是做什么的？",
    "如何保存 Agent 的记忆？",
]
for query in queries:
    print_results(query)
