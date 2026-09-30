from multi_query import generate_queries
from retriever import retriever


def multi_query_retrieve(question, retriever):
    queries = generate_queries(question)
    results = []
    for query in queries:
        result = retriever.invoke(query)
        results.append(result)
    return results
