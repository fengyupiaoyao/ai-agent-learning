from multi_query import generate_queries

question = "为什么 Agent 需要 Memory？"

queries = generate_queries(question)

for query in queries:
    print(query)
