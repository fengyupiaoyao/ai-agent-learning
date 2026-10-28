from evals.dataset import EVAL_CASES
from evals.runner import evaluate_answer


def main():
    answers = {
        "mcp-001": "MCP 是连接 AI 应用与工具的协议。",
        "mcp-002": "MCP Server 可以提供工具和资源。",
        "mcp-003": "工具没有找到结果时，应明确说明没有找到。",
    }

    results = []

    for case in EVAL_CASES:
        answer = answers[case["id"]]
        result = evaluate_answer(case, answer)
        results.append(result)

        print(
            f"{result.case_id} "
            f"passed={result.passed} "
            f"score={result.score:.2f} "
            f"reason={result.reason}"
        )
    pass_rate = sum(r.passed for r in results) / len(results)

    print(f"\n总案例数：{len(results)}")
    print(f"通过率：{pass_rate:.1%}")


if __name__ == "__main__":
    main()
