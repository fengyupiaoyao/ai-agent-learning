from langchain_core.tools import tool


@tool
def calcuator(expression: str) -> str:
    """
    A simple calculator tool that can add, subtract, multiply, and divide two numbers.
    """
    try:
        return str(eval(expression))
    except ZeroDivisionError:
        return "Error: Division by zero is not allowed."
    except Exception as e:
        return f"Error: {e}"


@tool
def get_user(user_id: str) -> str:
    """
    Get user information by user_id.
    """
    users = {
        "1001": {
            "name": "Alice",
            "role": "developer",
        },
        "1002": {
            "name": "Bob",
            "role": "designer",
        },
    }
    user = users.get(user_id)
    if not user:
        return "User not found."
    return str(user)


@tool
def search_python_docs(query: str) -> str:
    """
    Search the Python documentation for a given query.
    """

    docs = {
        "decorator": "Python 装饰器可以修改或增强函数行为。",
        "async": "async 和 await 用于 Python 异步编程。",
        "dataclass": "dataclass 用于快速定义数据类。",
    }
    query = query.lower()

    results = []

    for keyword, content in docs.items():
        if query in keyword:
            results.append(content)
    if not results:
        return "No results found."
    return "\n".join(results)


@tool
def is_developer(role: str) -> str:
    """Check whether a user role is developer."""

    if role == "developer":
        return "Yes, this user is a developer."

    return "No, this user is not a developer."
