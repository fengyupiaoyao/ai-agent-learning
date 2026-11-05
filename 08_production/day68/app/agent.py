from app.schemas import AgentRequest, RetrievedDocument
from app.security import SecurityPolicy
from app.prompt_builder import build_prompt
from app.mock_llm import MockLLM


class KnowledgeAgent:
    def __init__(self):
        self.security = SecurityPolicy()
        self.llm = MockLLM()

    def run(
        self,
        request: AgentRequest,
        documents: list[RetrievedDocument],
    ):
        request_result = self.security.validate_request(request)

        if not request_result["allowed"]:
            return {
                "status": "blocked",
                "reason": request_result["reason"],
            }

        document_texts = []

        for document in documents:
            result = self.security.validate_document(document)
            if not result["allowed"]:
                return {
                    "status": "blocked",
                    "reason": "文档校验失败",
                }
            document_texts.append(document.content)

        prompt = build_prompt(
            question=request.question,
            documents=document_texts,
        )

        output = self.llm.invoke(prompt)

        if not self.security.validate_output(output):
            return {
                "status": "blocked",
                "reason": "模型输出未通过校验",
            }

        return {
            "status": "success",
            "output": output,
        }
