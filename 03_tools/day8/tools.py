from langchain_core.tools import tool


@tool
def calculator(operation: str) -> str:
    """A simple calculator tool that can add, subtract, multiply, and divide two numbers."""
    return str(eval(operation))


@tool
def get_user_name(user_id: str) -> str:
    """Get the name of a user by their user ID."""

    users = {
        "1001": "John Doe",
        "1002": "Bob Smith"
    }

    return users.get(user_id, "User not found")
