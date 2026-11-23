class ResearchAgent:
    def run(self, task: str) -> str:
        return f"Research Agent 已完成资料收集：{task}"


class AnalysisAgent:
    def run(self, research_result: str) -> str:
        return f"Analysis Agent 已完成分析：{research_result}"


class ExecutionAgent:
    def run(self, task: str) -> str:
        return f"Execution Agent 收到执行任务：{task}"


class AgentTeam:
    def __init__(self):
        self.research = ResearchAgent()
        self.analysis = AnalysisAgent()
        self.execution = ExecutionAgent()

    def run_analysis(self, task: str) -> dict:
        research_result = self.research.run(task)
        analysis_result = self.analysis.run(research_result)
        return {
            "research_result": research_result,
            "analysis_result": analysis_result,
        }
