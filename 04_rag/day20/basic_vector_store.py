from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv

import os
load_dotenv()

embeddings = OpenAIEmbeddings(
    model="text-embedding-v3",
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://ws-wopagvlf3afu5baf.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
    check_embedding_ctx_length=False  # 禁用分词，直接发送原始文本
)

vector_store = Chroma(
    collection_name="agent_learning",
    embedding_function=embeddings,
    persist_directory="./chroma_db",
)

documents = [
    Document(page_content="RAG 是 Retrieval-Augmented Generation，通过检索外部知识增强 LLM。",
             metadata={"topic": "RAG"}, ),
    Document(page_content="AI Agent 可以使用工具执行搜索、计算、数据库查询等任务。",
             metadata={"topic": "Agent"}, ),
    Document(page_content="Python 是一种广泛用于人工智能和数据分析的编程语言。",
             metadata={"topic": "Python"}, ),
]

vector_store.add_documents(documents)

results = vector_store.similarity_search_with_score(
    "RAG 是什么？",
    k=2,
)
for doc, score in results:
    print(f"Score: {score}")
    print(doc.page_content)
    print(doc.metadata)
    print("-" * 80)
