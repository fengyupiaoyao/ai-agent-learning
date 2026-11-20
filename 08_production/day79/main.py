import json
from pathlib import Path

from app.runner import run_evaluation
from app.regression import detect_regressions
from app.comparison import compare_reports
from app.failure_analysis import analyze_failure, analyze_report
from app.release_gate import check_release_gate


DATASET = "data/eval_dataset.json"


def save_json(path: str, data: dict):
    Path(path).parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            data,
            file,
            indent=2,
            ensure_ascii=False
        )


def main():
    # 1. 执行 V1
    v1 = run_evaluation(DATASET, "v1")

    # 2. 执行 V2
    v2 = run_evaluation(DATASET, "v2")

    # 3. 回归检测
    regression = detect_regressions(v1, v2)

    # 4. 版本对比
    comparison = compare_reports(v1, v2)

    # 5. 失败分析
    failures = analyze_report(v2)

    # 6. 保存报告
    save_json("reports/v1_report.json", v1)
    save_json("reports/v2_report.json", v2)

    save_json(
        "reports/comparison_report.json",
        {
            "regression": regression,
            "comparison": comparison,
            "failures": failures
        }
    )

    print("\n===== V1 =====")
    print(v1["summary"])

    print("\n===== V2 =====")
    print(v2["summary"])

    print("\n===== Regression =====")
    print(json.dumps(
        regression,
        indent=2,
        ensure_ascii=False
    ))

    print("\n===== Failure Analysis =====")
    print(json.dumps(
        failures,
        indent=2,
        ensure_ascii=False
    ))

    gate = check_release_gate(
        v2,
        regression
    )

    print("\n===== Release Gate =====")
    print(gate)


if __name__ == "__main__":
    main()
