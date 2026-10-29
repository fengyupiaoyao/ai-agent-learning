import json
import sys

from pathlib import Path

from evals.quality_gate import (
    QualityThresholds, check_quality
)


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: run_quality_gate.py <metrics.json>")
    path = Path(sys.argv[1])

    try:
        metrics = json.loads(path.read_text(encoding="utf-8"))
        failures = check_quality(metrics, QualityThresholds())
    except (OSError, json.JSONDecodeError, KeyError, TypeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    if failures:
        print("Quality gate failed:", *failures, sep="\n", file=sys.stderr)
        return 1

    print("Quality gate passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
