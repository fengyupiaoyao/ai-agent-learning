from pydantic import BaseModel, Field


class TutorResponse(BaseModel):
    explanation: str = Field(
        description="对 Python 概念进行清晰解释"
    )

    example: str = Field(
        description="一个简单易懂的 Python 代码示例"
    )

    common_mistakes: list[str] = Field(
        description="学习这个知识点时常见的错误"
    )

    exercise: str = Field(
        description="一道帮助用户练习的题目"
    )
