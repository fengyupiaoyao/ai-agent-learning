def reciprocal_rank(
    retriever,
    question,
    expected_source,
):
    docs = retriever.invoke(question)

    for rank, doc in enumerate(docs, start=1):
        if doc.metadata["source"] == expected_source:
            return 1 / rank
    return 0


def evaluate_mrr(
    retriever,
    dataset,
):
    scores = []

    for case in dataset:
        score = reciprocal_rank(
            retriever,
            case.question,
            case.expected_source,
        )
        scores.append(score)
    return sum(scores) / len(scores)
