from app.orchestrator import AgentOrchestrator, resume
from app.evaluation import evaluate_result
from app.release_gate import check_release


def main():
    agent = AgentOrchestrator()

    result = agent.run(
        task_id="task-001",
        user_input="分析 LangGraph Checkpoint 的作用",
    )

    print("\n普通任务结果：")
    print(result)

    pending = agent.run(
        task_id="task-002",
        user_input="删除旧文件",
        approved=False,
    )

    print("\n审批等待结果：")
    print(pending)

    resumed = resume(
        task_id="task-002",
        approved=True,
    )

    print("\n恢复结果：")
    print(resumed)

    # 评测
    evaluation_results = [
        evaluate_result(result),
        evaluate_result(resumed),
    ]

    # 发布门禁
    release = check_release(
        evaluation_results=evaluation_results,
        regression_detected=False,
        safety_passed=True,
    )

    print("\n发布门禁：")
    print(release)


if __name__ == "__main__":
    main()
