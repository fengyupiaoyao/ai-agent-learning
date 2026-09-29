from reciprocal_rank import evaluate_mrr
from retriever import retriever
from dataset import dataset

score = evaluate_mrr(retriever, dataset)

print("MRR score: ", score)
