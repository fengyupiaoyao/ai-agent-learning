from rewrite import rewrite_query

questions = [
    "Agent 怎么操作外部东西？",
    "RAG 为什么有时候搜不到东西？",
    "Memory 到底是干嘛的？",
]

for question in questions:
    rewritten_question = rewrite_query(question)
    print("=" * 60)
    print(f"Original: {question}")
    print(f"Rewritten: {rewritten_question}")
