class MockLLM:

    def invoke(self, prompt: str):
        if "请总结" in prompt:
            return "这份文档主要介绍了 Agent 安全与 Prompt Injection。"

        return "我无法根据当前资料提供可靠答案。"
