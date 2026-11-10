from app.models import UserContext, ToolCall
from app.tool_router import ToolRouter


def main():
    router = ToolRouter()

    viewer = UserContext(
        user_id="user_001",
        role="viewer",
    )

    researcher = UserContext(
        user_id="user_002",
        role="researcher",
    )

    operator = UserContext(
        user_id="user_003",
        role="operator",
    )

    result = router.execute(
        viewer,
        ToolCall(
            tool_name="search_docs",
            arguments={"query": "LangGraph"},
        )
    )

    print("场景1：", result)

    result = router.execute(
        viewer,
        ToolCall(
            tool_name="delete_file",
            arguments={"file_id": "file_001"},
        )
    )

    print("场景2：", result)

    result = router.execute(
        researcher,
        ToolCall(
            tool_name="read_file",
            arguments={"file_id": "file_001"},
        )
    )

    print("场景3：", result)

    email_call = ToolCall(
        tool_name="send_email",
        arguments={
            "to": "test@example.com",
            "subject": "Test",
            "body": "Hello",
        },
    )

    result = router.execute(operator, email_call)
    print("场景 4:", result)

    router.approval.approve("approval_001")

    result = router.execute(
        operator,
        email_call,
        approval_id="approval_001",
    )
    print("场景 5:", result)


if __name__ == "__main__":
    main()
