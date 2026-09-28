import os
from dotenv import load_dotenv
from openai import OpenAI

# 加载 .env 文件
load_dotenv()

# 通义千问 API 配置
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://ws-wopagvlf3afu5baf.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)

texts = [
    "RAG 是什么？",
    "什么是 Retrieval-Augmented Generation？",
    "今天天气怎么样？",
]

for text in texts:
    response = client.embeddings.create(
        model="text-embedding-v3",
        input=text
    )
    vector = response.data[0].embedding

    print("=" * 50)
    print(f"Text: {text}")
    print(f"Vector: {vector}")
