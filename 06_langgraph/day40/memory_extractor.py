from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI

from memory_service import save_memory, search_memory

import os
from dotenv import load_dotenv

load_dotenv()


class MemoryFact(BaseModel):
    content: str = Field(
        description="简洁、独立、可复用的记忆内容",
    )
    category: str = Field(
        description="记忆分类，例如 preference、skill、goal、project"
    )


class MemoryExtraction(BaseModel):
    memories: list[MemoryFact] = Field(
        description="值得长期保存的记忆列表；没有则返回空列表"
    )


extractor = ChatOpenAI(
    model="qwen3.8-max",
    api_key=os.environ["OPENAI_API_KEY"],
    base_url="https://ws-wopagvlf3afu5baf.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
    temperature=0,
).with_structured_output(MemoryExtraction)


def extract_and_save(
    user_id: str,
    conversation: str,
) -> list[str]:
    results = extractor.invoke([
        (
            "system",
            """
            你负责提取用户的长期记忆。

            只提取明确表达、未来可能有帮助的信息，例如：
            - 长期学习目标
            - 稳定的回答偏好
            - 已掌握的技能
            - 正在进行的长期项目

            不要提取：
            - 一次性问题或普通闲聊
            - 没有依据的推断
            - 密码、API Key 等秘密
            - 没有必要长期保存的敏感信息

            每条记忆应简洁、独立、可复用。
            不确定是否值得保存时，宁可不保存。
            """
        ),
        ("human", conversation),
    ])

    saved = []

    for fact in results.memories:
        memory_id = save_memory(
            user_id,
            fact.content,
            fact.category,
        )
        saved.append(memory_id)

    return saved


if __name__ == "__main__":
    conversation = """
    我最近在系统学习 AI Agent，已经会 Python。
    我希望讲解技术时先给出完整代码，再解释原理。
    今天帮我计算一下 17 乘以 23。
    """

    ids = extract_and_save("user_123", conversation)

    print("Saved memory IDs:", ids)
