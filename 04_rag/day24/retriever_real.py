from retriever import retriever


def hit_at_k(
    retriever,
    question: str,
    expected_source: str,
) -> bool:
    docs = retriever.invoke(question)

    sources = [
        doc.metadata["source"]
        for doc in docs
    ]

    return expected_source in sources
