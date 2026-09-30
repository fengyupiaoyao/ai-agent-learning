from rewrite import rewrite_query
from retriever import retriever
from rich import print as pprint


def retrieve_with_rewrite(question: str, retriever):
    rewritten_question = rewrite_query(question)
    return retriever.invoke(rewritten_question)


if __name__ == "__main__":
    question = "Agent 怎么操作外部东西？"
    result = retrieve_with_rewrite(question, retriever)
    pprint(result)
