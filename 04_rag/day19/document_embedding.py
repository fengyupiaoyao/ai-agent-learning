from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

import os

from pathlib import Path

load_dotenv()

file_path = Path(__file__).resolve().parent / "data" / "rag.md"

loader = TextLoader(
    file_path,
    encoding="utf-8"
)

documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=0
)

chunks = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings(
    model="text-embedding-v3",
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://ws-wopagvlf3afu5baf.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
    check_embedding_ctx_length=False  # 禁用分词，直接发送原始文本
)

texts = [
    chunk.page_content for chunk in chunks
]

vectors = embeddings.embed_documents(texts)

print(vectors)
