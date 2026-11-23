def request_approval(
    tool_name: str,
    approved: bool = False,
) -> bool:
    print(f"等待人工审批：{tool_name}")

    if not approved:
        print("审批未通过，禁止执行")
        return False

    print("审批通过")
    return True
