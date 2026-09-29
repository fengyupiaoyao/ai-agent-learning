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

    retriever = vector_store.as_retriever(
        # search_type="similarity",
        # search_kwargs={"k": 3}
        search_type="mmr",
        search_kwargs={"k": 3, "fetch_k": 10}
    )
    return retriever


if __name__ == "__main__":
    retriever = create_retriever()

    docs = retriever.invoke("Agent 如何保存长期记忆？")

    for i, doc in enumerate(docs):
        print(f"Document {i+1}:")
        print(f"  Page Content: {doc.page_content}")
        print(f"  Metadata: {doc.metadata}")
        print("=" * 50)
