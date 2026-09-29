from retriever import vector_store

query = "Agent 如何保存记忆？"

for k in [1, 2, 3, 5]:
    # results = vector_store.similarity_search(
    #     query,
    #     k=k
    # )

    # print("\n")
    # print("=" * 60)
    # print("k={}".format(k))
    # print("=" * 60)

    # for i, doc in enumerate(results):
    #     print(i, doc.metadata["topic"])

    results = vector_store.similarity_search_with_score(
        query,
        k=5
    )
    for doc, score in results:
        print("topic:", doc.metadata["topic"], "score:", score)
