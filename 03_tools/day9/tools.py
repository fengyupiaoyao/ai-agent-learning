from unittest import result
from langchain_core.tools import tool
from datetime import datetime
from pydantic import BaseModel, Field

PYTHON_DOCS = {
    "decorator": """
Python 装饰器是一种可以修改或增强函数行为的机制。
常见形式是 @decorator。
""",

    "async": """
async 和 await 用于 Python 异步编程。
async 定义协程函数，await 等待异步操作完成。
""",

    "dataclass": """
dataclass 可以帮助开发者快速定义主要用于保存数据的类。
"""
}

USERS = {
    "1001": {
        "name": "Alice",
        "role": "developer",
    },
    "1002": {
        "name": "Bob",
        "role": "designer",
    },
}


@tool
def calculate(expression: str) -> str:
    """
    Calculate the result of an expression.
    """
    return str(eval(expression))

# print(calculate.name)
# print(calculate.description)
# print(calculate.args)


@tool
def search_python_docs(query: str) -> str:
    """
    Search the local Python documentation.

    Use this tool when the user asks about
    Python syntax, Python language features,
    or standard Python concepts.
    """

    query = query.lower

    results = []

    for keyword, content in PYTHON_DOCS.items():
        if keyword in query:
            results.append(content)
    if not results:
        return "No results found."

    return "\n".join(results)


@tool
def get_user(user_id: str) -> str:
    """
    Get user information by user ID.
    """
    user = USERS.get(user_id)

    if not user:
        return "User not found."

    return str(user)


@tool
def get_current_time() -> str:
    """
    Get the current time.
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class UserSearchInput(BaseModel):
    keyword: str = Field(
        description="The keyword to search for in user names.")

    role: str | None = Field(
        default=None,
        description="The role to filter users by."
    )

    limit: int = Field(
        default=10,
        ge=1,
        le=100,
        description="The maximum number of results to return."
    )


@tool(args_schema=UserSearchInput)
def search_users(
    keyword: str,
    role: str | None = None,
    limit: int = 10,
) -> str:
    """
    Search for users by keyword, role, and limit.
    """

    users = [
        {
            "id": "1001",
            "name": "Alice",
            "role": "developer",
        },
        {
            "id": "1002",
            "name": "Bob",
            "role": "designer",
        },
        {
            "id": "1003",
            "name": "Charlie",
            "role": "developer",
        },
    ]
    results = []

    for user in users:
        if keyword.lower() not in user["name"].lower():
            continue
        if role and user["role"] != role:
            continue
        results.append(user)
        if len(results) >= limit:
            break
    return str(results)
