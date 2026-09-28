from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv

import os
from pathlib import Path

load_dotenv()

file_path = Path(__file__).resolve().parent / "data" / "rag.md"


def build_vector_store():
    loader = TextLoader(file_path, encoding="utf-8")
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=0)
    documents = text_splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings(
        model="text-embedding-v3",
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url="https://ws-wopagvlf3afu5baf.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
        check_embedding_ctx_length=False  # 禁用分词，直接发送原始文本
    )

    vector_store = Chroma.from_documents(
        documents,
        embeddings,
        persist_directory="./chroma_db",
        collection_name="agent_learning"  # 指定集合名称
    )

    return vector_store


if __name__ == "__main__":
    vector_store = build_vector_store()
