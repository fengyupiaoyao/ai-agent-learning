from dataclasses import dataclass


@dataclass(frozen=True)
class QualityThresholds:
    min_pass_rate: float = 0.85
    max_latency_ms: float = 3000.0
    max_failure_rate: float = 0.10


def check_quality(
    metrics: dict,
    thresholds: QualityThresholds,
) -> list[str]:
    """返回所有不满足门槛的原因；空列表表示通过。"""
    failures = []

    pass_rate = metrics["pass_rate"]
    latency_ms = metrics["latency_ms"]
    failure_rate = metrics["failure_rate"]

    if not 0 <= pass_rate <= 1:
        failures.append("pass_rate 必须在 0 到 1 之间")

    if not 0 <= failure_rate <= 1:
        failures.append("failure_rate 必须在 0 到 1 之间")

    if latency_ms < 0:
        failures.append("latency_ms 不能为负数")

    # 输入不合法时，不再进行门槛判断
    if failures:
        return failures

    if pass_rate < thresholds.min_pass_rate:
        failures.append(
            f"通过率过低：{pass_rate:.1%} "
            f"< {thresholds.min_pass_rate:.1%}"
        )

    if latency_ms > thresholds.max_latency_ms:
        failures.append(
            f"延迟过高：{latency_ms:.0f} ms "
            f"> {thresholds.max_latency_ms:.0f} ms"
        )

    if failure_rate > thresholds.max_failure_rate:
        failures.append(
            f"失败率过高：{failure_rate:.1%} "
            f"> {thresholds.max_failure_rate:.1%}"
        )

    return failures
