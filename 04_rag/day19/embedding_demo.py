from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

import os

from pathlib import Path

load_dotenv()

file_path = Path(__file__).resolve().parent / "data" / "rag.md"


def load_document():
    loader = TextLoader(
        file_path,
        encoding="utf-8"
    )
    return loader.load()


def split_documents(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=0
    )
    return text_splitter.split_documents(documents)


def embed_documents(chunks):
    return OpenAIEmbeddings(
        model="text-embedding-v3",
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url="https://ws-wopagvlf3afu5baf.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
        check_embedding_ctx_length=False  # 禁用分词，直接发送原始文本
    ).embed_documents([chunk.page_content for chunk in chunks])


def main():
    documents = load_document()
    chunks = split_documents(documents)
    embeddings = embed_documents(chunks)
    if embeddings is not None:
        print(embeddings)


if __name__ == "__main__":
    main()
