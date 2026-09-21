from langchain_openai import ChatOpenAI

from models import TutorResponse
from prompts import tutor_prompt


class PythonTutor:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="qwen-plus",
            base_url="https://ws-wopagvlf3afu5baf.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
        )

        structured_model = self.llm.with_structured_output(TutorResponse)

        self.chain = tutor_prompt | structured_model

    def ask(self, question: str) -> TutorResponse:
        return self.chain.invoke({"question": question})
