import json
import sys

from pathlib import Path

RESULT_DIR = Path(__file__).resolve().parent / "results"


def load_result(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def compare(a: dict, b: dict) -> dict:
    ma = a["metrics"]
    mb = b["metrics"]

    # 防止比较不同数据集或不同评分规则的结果
    if a["dataset_version"] != b["dataset_version"]:
        raise ValueError("数据集版本不同，不能直接比较")

    if a["evaluator_version"] != b["evaluator_version"]:
        raise ValueError("评测器版本不同，不能直接比较")

    return {
        "baseline": a["agent_version"],
        "candidate": b["agent_version"],
        "pass_rate_delta": round(
            mb["pass_rate"] - ma["pass_rate"], 4
        ),
        "latency_delta_ms": (
            mb["latency_ms"] - ma["latency_ms"]
        ),
        "estimated_cost_delta_usd": round(
            mb["estimated_cost_usd"]
            - ma["estimated_cost_usd"],
            6,
        ),
        "config_changed": (
            a["config_fingerprint"] != b["config_fingerprint"]
        ),
    }


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit(
            "Usage: compare_experiments.py <result_a.json> <result_b.json>")

    a = load_result(RESULT_DIR / sys.argv[1])
    b = load_result(RESULT_DIR / sys.argv[2])

    report = compare(a, b)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
