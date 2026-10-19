from langchain_openai import OpenAIEmbeddings

import os
from dotenv import load_dotenv

load_dotenv()

embeddings = OpenAIEmbeddings(
    model="text-embedding-v3",
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://ws-wopagvlf3afu5baf.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
    check_embedding_ctx_length=False  # 禁用分词，直接发送原始文本
)


def similarity(a, b):
    va = embeddings.embed_query(a)

    vb = embeddings.embed_query(b)

    dot = sum(
        x * y
        for x, y in zip(va, vb)
    )

    return dot


print(
    similarity(
        "我喜欢代码优先教学",
        "我喜欢先看代码再学习"
    )
)
