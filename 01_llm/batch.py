import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# 按脚本位置加载项目根目录的配置，不依赖运行目录
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

model = ChatOpenAI(
    model="qwen-plus",
    api_key=os.environ["OPENAI_API_KEY"],
    base_url="https://ws-wopagvlf3afu5baf.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

response = model.batch(["介绍一下RAG", "你是谁"])

# response 是一个 list[AIMessage]，逐个解析
for i, msg in enumerate(response):
    print(f"--- 第{i+1}个回答 ---")
    print(f"内容: {msg.content}")                # 文本内容
    print(f"Token用量: {msg.usage_metadata}")     # token 统计
    print()
