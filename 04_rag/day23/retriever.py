from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings

from splitter import split_documents

import os
from dotenv import load_dotenv

load_dotenv()

embeddings = OpenAIEmbeddings(
    model="text-embedding-v3",
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://ws-wopagvlf3afu5baf.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
    check_embedding_ctx_length=False  # 禁用分词，直接发送原始文本
)
vector_store = InMemoryVectorStore(embedding=embeddings)

vector_store.add_documents(split_documents)
