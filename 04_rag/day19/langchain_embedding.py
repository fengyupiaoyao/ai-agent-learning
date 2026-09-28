import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings


load_dotenv()

embeddings = OpenAIEmbeddings(
    model="text-embedding-v3",
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://ws-wopagvlf3afu5baf.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
    check_embedding_ctx_length=False  # 禁用分词，直接发送原始文本
)

query_vector = embeddings.embed_query("RAG是什么？")

document_vectors = embeddings.embed_documents(
    [
        "RAG是什么？",
        "Retrieval-Augmented Generation是什么？",
        "RAG如何增强大语言模型？",
        "今天东京天气怎么样？"
    ]
)

print("Query Vector:", query_vector)
print("Document Vectors:", document_vectors)
