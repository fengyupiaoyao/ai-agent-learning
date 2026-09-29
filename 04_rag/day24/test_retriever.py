from retriever import retriever
from dataset import dataset
from retriever_real import hit_at_k

for case in dataset:
    hit = hit_at_k(
        retriever,
        case.question,
        case.expected_source,
    )

    print(
        case.question,
        "->",
        hit
    )
