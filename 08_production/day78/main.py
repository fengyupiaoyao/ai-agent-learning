import json
from pathlib import Path

from app.runner import run_evaluation


report = run_evaluation(
    "data/eval_dataset.json"
)

print("\n===== Evaluation Summary =====")

print(
    json.dumps(
        report["summary"],
        indent=2,
        ensure_ascii=False
    )
)

print("\n===== Case Results =====")

for item in report["results"]:
    print(
        item["id"],
        item["total_score"],
        "PASS" if item["passed"] else "FAIL"
    )

Path("reports").mkdir(exist_ok=True)

with open(
    "reports/evaluation_report.json",
    "w",
    encoding="utf-8"
) as file:
    json.dump(
        report,
        file,
        indent=2,
        ensure_ascii=False
    )

print("\nReport saved.")
