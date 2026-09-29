from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

from retriever import create_retriever
from prompts import prompt

from operator import itemgetter

import os
from dotenv import load_dotenv

load_dotenv()


def format_docs(docs):
    return "\n".join([doc.page_content for doc in docs])


retriever = create_retriever()

llm = ChatOpenAI(
    model="qwen3.8-max",
    api_key=os.environ["OPENAI_API_KEY"],
    base_url="https://ws-wopagvlf3afu5baf.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
    temperature=0,
)

# docs = retriever.invoke(question)
# context = format_docs(docs)
# prompt_value = prompt.invoke(
#     {
#         "context": context,
#         "question": question,
#     }
# )

# response = llm.invoke(prompt_value)
# answer = parser.invoke(response)

rag_chain = (
    {
        "context": itemgetter("question")
        | retriever
        | format_docs,

        "question": itemgetter("question"),
    }
    | prompt
    | llm
    | StrOutputParser()
)


def ask(question: str):
    return rag_chain.invoke({"question": question})


def retrieve_with_sources(question):
    docs = retriever.invoke(question)
    return {
        "answer": rag_chain.invoke({"question": question}),
        "sources": [
            doc.metadata for doc in docs
        ]
    }


if __name__ == "__main__":
    # response = ask("Agent Memory 是什么？")
    response = ask("Langchain 作者是谁？")
    print(response)

    print("=" * 60)

    response = retrieve_with_sources("Agent Memory 是什么？")
    print(response)
