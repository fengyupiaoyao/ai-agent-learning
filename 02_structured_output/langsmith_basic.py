import os
from pathlib import Path
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
# 按脚本位置加载项目根目录的配置，不依赖运行目录
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

model = ChatOpenAI(
    model="qwen-plus",
    api_key=os.environ["OPENAI_API_KEY"],
    base_url="https://ws-wopagvlf3afu5baf.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            你是一名 Python Tutor。

            你的任务是帮助用户学习 Python。

            回答要求：
            1. 使用中文
            2. 先解释概念
            3. 给出简单代码
            4. 说明常见错误
            """
        ),
        (
            "human",
            "{question}"
        ),
    ]
)

chain = prompt | model


def ask(question: str):
    response = chain.invoke(
        {"question": question},
        config={
            "tags": ["day6", "python-tutor"],
            "metadata": {
                "course": "ai-agent-learning",
                "day": "6",
            }
        }
    )
    return response


if __name__ == "__main__":
    question = "Python 中的列表推导式是什么？"
    response = ask(question)

    print("\n AI Tutor:")
    print(response)
