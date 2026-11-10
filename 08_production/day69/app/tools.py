from typing import Any


class ToolRegistry:
    def __init__(self):
        self.tools = {
            "search_docs": {
                "required": {"query"},
                "allowed": {"query"},
                "high_risk": False,
                "handler": self.search_docs,
            },

            "read_file": {
                "required": {"file_id"},
                "allowed": {"file_id"},
                "high_risk": False,
                "handler": self.read_file,
            },

            "send_email": {
                "required": {"to", "subject", "body"},
                "allowed": {"to", "subject", "body"},
                "high_risk": True,
                "handler": self.send_email,
            },

            "delete_file": {
                "required": {"file_id"},
                "allowed": {"file_id"},
                "high_risk": True,
                "handler": self.delete_file,
            },
        }

    def search_docs(self, query: str):
        return {
            "tool": "search_docs",
            "query": query,
            "results": ["doc_001", "doc_002"],
        }

    def read_file(self, file_id: str):
        return {
            "tool": "read_file",
            "file_id": file_id,
            "content": "Mock document content",
        }

    def send_email(
        self,
        to: str,
        subject: str,
        body: str,
    ):
        return {
            "tool": "send_email",
            "status": "mock_sent",
            "to": to,
        }

    def delete_file(self, file_id: str):
        return {
            "tool": "delete_file",
            "status": "mock_deleted",
            "file_id": file_id,
        }
