from retriever_real import hit_at_k


def evaluate_recall(
    retriever,
    dataset,
):
    hits = 0

    for case in dataset:
        if hit_at_k(
            retriever,
            case.question,
            case.expected_source,
        ):
            hits += 1
    return hits / len(dataset)
