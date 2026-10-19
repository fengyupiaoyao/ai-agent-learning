from langchain_openai import ChatOpenAI
from memory_models import MemoryItem

from pydantic import BaseModel

import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(
    model="qwen3.8-max",
    api_key=os.environ["OPENAI_API_KEY"],
    base_url="https://ws-wopagvlf3afu5baf.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
    temperature=0,
)


class MemoryDecision(BaseModel):
    should_save: bool
    importance: int
    reason: str


evaluator = llm.with_structured_output(
    MemoryDecision
)


def evaluate_memory(text):
    result = evaluator.invoke(
        f"""
        判断下面信息是否值得长期保存。

        信息:
        {text}


        保存标准:

        值得保存:
        - 用户技能
        - 长期目标
        - 稳定偏好
        - 长期项目


        不保存:
        - 临时问题
        - 一次计算
        - 普通聊天

        """
    )
    return result


print(evaluate_memory("我喜欢回答先给代码，再解释"))
