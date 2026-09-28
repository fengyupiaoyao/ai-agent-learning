import os
import math

from dotenv import load_dotenv
from openai import OpenAI

# 加载 .env 文件
load_dotenv()

# 通义千问 API 配置
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://ws-wopagvlf3afu5baf.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)


def embed(text):
    response = client.embeddings.create(
        model="text-embedding-v3",
        input=text
    )
    return response.data[0].embedding


def cosine_similarity(a, b):
    dot_product = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x ** 2 for x in a))
    norm_b = math.sqrt(sum(x ** 2 for x in b))
    return dot_product / (norm_a * norm_b)


texts = [
    "RAG 是什么？",
    "什么是 Retrieval-Augmented Generation？",
    "RAG 如何增强大语言模型？",
    "今天东京天气怎么样？",
]

query = embed(texts[0])

for text in texts:
    vector = embed(text)

    score = cosine_similarity(query, vector)
    print(f"Text: {text}")
    print(f"Score: {score}")
