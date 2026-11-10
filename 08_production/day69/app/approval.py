class ApprovalService:
    def __init__(self):
        self.approval_ids = set()

    def request_approval(self, approval_id: str):
        return {
            "approval_id": approval_id,
            "status": "pending",
        }

    def approve(self, approval_id: str):
        self.approval_ids.add(approval_id)

    def is_approved(self, approval_id: str) -> bool:
        return approval_id in self.approval_ids
