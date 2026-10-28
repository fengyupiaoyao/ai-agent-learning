import asyncio
import json
import time
from pathlib import Path

from app.services.research_service import ResearchService
from evals.dataset import EVAL_CASES
from evals.runner import evaluate_answer


async def main():
    service = ResearchService()
    results = []

    try:
        for case in EVAL_CASES:
            started = time.perf_counter()

            try:
                answer = await service.run(case["question"])
                evaluation = evaluate_answer(case, answer)

                row = {
                    "case_id": case["id"],
                    "passed": evaluation.passed,
                    "score": evaluation.score,
                    "reason": evaluation.reason,
                    "duration_ms": round(
                        (time.perf_counter() - started) * 1000,
                        2,
                    ),
                }
            except Exception as e:
                row = {
                    "case_id": case["id"],
                    "passed": False,
                    "score": 0.0,
                    "reason": type(e).__name__,
                    "duration_ms": round(
                        (time.perf_counter() - started) * 1000,
                        2,
                    ),
                }
            results.append(row)
            print(row)
    finally:
        output = Path("evals/results.json")
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(
            json.dumps(results, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    if results:
        passed = sum(row["passed"] for row in results)
        print(f"通过率：{passed / len(results):.1%}")
        print("结果已保存到 evals/results.json")

if __name__ == "__main__":
    asyncio.run(main())
