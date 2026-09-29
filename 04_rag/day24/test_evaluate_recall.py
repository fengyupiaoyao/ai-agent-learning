from retriever import retriever
from dataset import dataset
from evaluate_recall import evaluate_recall

score = evaluate_recall(retriever, dataset)

print(
    "Recall score: ",
    score
)
