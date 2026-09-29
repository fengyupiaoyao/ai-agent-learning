from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings

from data.knowledge import documents

import os
from dotenv import load_dotenv

load_dotenv()


def create_retriever():
    embeddings = OpenAIEmbeddings(
        model="text-embedding-v3",
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url="https://ws-wopagvlf3afu5baf.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
        check_embedding_ctx_length=False  # 禁用分词，直接发送原始文本
    )

    vector_store = InMemoryVectorStore(
        embedding=embeddings,
    )

    vector_store.add_documents(documents)

    return vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3}
    )
