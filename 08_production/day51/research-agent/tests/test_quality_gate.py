import pytest

from evals.quality_gate import (
    QualityThresholds,
    check_quality,
)


@pytest.fixture
def thresholds():
    return QualityThresholds(
        min_pass_rate=0.85,
        max_latency_ms=3000,
        max_failure_rate=0.10,
    )


def test_quality_gate_passes(thresholds):
    metrics = {
        "pass_rate": 0.90,
        "latency_ms": 1200,
        "failure_rate": 0.05,
    }

    assert check_quality(metrics, thresholds) == []


def test_quality_gate_rejects_low_pass_rate(thresholds):
    metrics = {
        "pass_rate": 0.70,
        "latency_ms": 1200,
        "failure_rate": 0.05,
    }

    failures = check_quality(metrics, thresholds)

    assert any("通过率过低" in item for item in failures)


def test_quality_gate_rejects_slow_agent(thresholds):
    metrics = {
        "pass_rate": 0.90,
        "latency_ms": 3500,
        "failure_rate": 0.05,
    }

    failures = check_quality(metrics, thresholds)

    assert any("延迟过高" in item for item in failures)


def test_quality_gate_rejects_invalid_metric(thresholds):
    metrics = {
        "pass_rate": 1.2,
        "latency_ms": 1200,
        "failure_rate": 0.05,
    }

    failures = check_quality(metrics, thresholds)

    assert any("pass_rate 必须在 0 到 1 之间" in item
               for item in failures)
