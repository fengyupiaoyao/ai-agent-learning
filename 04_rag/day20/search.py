from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

import os
from dotenv import load_dotenv

load_dotenv()


def search_vector_store(query):
    embeddings = OpenAIEmbeddings(
        model="text-embedding-v3",
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url="https://ws-wopagvlf3afu5baf.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
        check_embedding_ctx_length=False  # 禁用分词，直接发送原始文本
    )
    vector_store = Chroma(
        collection_name="agent_learning",
        embedding_function=embeddings,
        persist_directory="./chroma_db"
    )

    results = vector_store.similarity_search(query, k=2)
    print(f"Found {len(results)} results:")
    for i, result in enumerate(results):
        print(f"Result {i+1}:")
        print(result.page_content)
        print("-" * 80)


if __name__ == "__main__":
    search_vector_store("RAG 是什么？")
