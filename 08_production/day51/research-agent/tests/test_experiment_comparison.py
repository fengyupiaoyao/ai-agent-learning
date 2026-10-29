import pytest

from experiments.compare_experiments import compare


def make_result(
    version: str,
    dataset: str = "eval-v1",
    evaluator: str = "keyword-v1",
) -> dict:
    return {
        "agent_version": version,
        "dataset_version": dataset,
        "evaluator_version": evaluator,
        "config_fingerprint": version,
        "metrics": {
            "passed": 8,
            "total": 10,
            "pass_rate": 0.8,
            "latency_ms": 800,
            "estimated_cost_usd": 0.01,
        },
    }


def test_compare_same_evaluation_setup():
    baseline = make_result("agent_v1")
    candidate = make_result("agent_v2")

    report = compare(baseline, candidate)

    assert report["pass_rate_delta"] == 0
    assert report["latency_delta_ms"] == 0
    assert report["config_changed"] is True


def test_reject_different_dataset():
    baseline = make_result("agent_v1")
    candidate = make_result("agent_v2", dataset="eval-v2")

    with pytest.raises(ValueError, match="数据集版本不同"):
        compare(baseline, candidate)


def test_reject_different_evaluator():
    baseline = make_result("agent_v1")
    candidate = make_result("agent_v2", evaluator="judge-v2")

    with pytest.raises(ValueError, match="评测器版本不同"):
        compare(baseline, candidate)
