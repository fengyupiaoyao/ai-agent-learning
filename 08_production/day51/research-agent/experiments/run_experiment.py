import hashlib
import json

from datetime import datetime, timezone
from pathlib import Path
from re import T

BASE_DIR = Path(__file__).resolve().parent
CONFIG_DIR = BASE_DIR / "configs"
RESULT_DIR = BASE_DIR / "results"


def load_config(version: str) -> dict:
    path = CONFIG_DIR / f"{version}.json"
    return json.loads(path.read_text(encoding="utf-8"))


def config_fingerprint(config: dict) -> str:
    content = json.dumps(
        config,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def run_experiment(version: str) -> dict:
    config = load_config(version)
    fingerprint = config_fingerprint(config)

    mock_results = {
        "agent_v1": {
            "passed": 8,
            "total": 10,
            "latency_ms": 820,
            "estimated_cost_usd": 0.012,
        },
        "agent_v2": {
            "passed": 9,
            "total": 10,
            "latency_ms": 880,
            "estimated_cost_usd": 0.014,
        },
    }

    if version not in mock_results:
        raise ValueError(f"Invalid version: {version}")

    metrics = mock_results[version]

    result = {
        "run_id": (
            f"{version}-"
            + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        ),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "agent_version": config["version"],
        "config_fingerprint": fingerprint,
        "model": config["model"]["name"],
        "prompt_version": config["prompt"]["version"],
        "dataset_version": config["dataset_version"],
        "evaluator_version": config["evaluator_version"],
        "metrics": {
            **metrics,
            "pass_rate": metrics["passed"] / metrics["total"],
        },
        "simulation": True,
    }

    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = RESULT_DIR / f"{result['run_id']}.json"
    output_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"Result saved to {output_path}")
    return result


async def evaluate_real_agent(agent, eval_cases):
    """
    真实评测时还需要补充：
        - 成本统计： 优先读取模型响应中的 token 使用量，并按对应模型的价格计算；无法获取时标记为未知，不要填入假值。
        - 失败记录： 保存案例 ID、错误类型、工具调用轨迹和评分理由，避免只看总分。
        - 重复运行： 对存在随机性的模型进行多轮评测，记录每轮结果与均值。
        - 版本追踪： 把 Git commit、Prompt 指纹、数据集版本和模型参数写入结果文件。
        - 安全： 不在实验报告中保存 API Key、Authorization 头或不必要的用户敏感数据。
    """
    passed = 0
    total = len(eval_cases)
    start = time.perf_counter()

    for case in eval_cases:
        # 按照项目当前的 Agent 接口执行
        answer = await agent.ainvoke({
            "messages": [
                {"role": "user", "content": case["question"]}
            ]
        })

        # 这里接入 Day 50 的评分函数。
        # score_answer 必须返回布尔值，表示该案例是否通过。
        if score_answer(answer, case):
            passed += 1

    elapsed_ms = (time.perf_counter() - start) * 1000

    return {
        "passed": passed,
        "total": total,
        "pass_rate": passed / total if total else 0.0,
        "latency_ms": round(elapsed_ms, 2),
    }

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--version",
        required=True,
        choices=["agent_v1", "agent_v2"],
    )

    args = parser.parse_args()
    run_experiment(args.version)
