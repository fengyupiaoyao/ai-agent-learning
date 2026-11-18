class ApprovalManager:
    def request_approval(
        self,
        tool_name: str,
        arguments: dict,
    ) -> bool:
        print("\n===== APPROVAL REQUIRED =====")
        print(f"Tool: {tool_name}")
        print(f"Arguments: {arguments}")

        answer = input("Approve? [y/N]: ")

        return answer.lower() == "y"
