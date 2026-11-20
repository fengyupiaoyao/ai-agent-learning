import json

from app.agent import run_agent
from app.evaluators import (
    evaluate_correctness,
    evaluate_tool_usage,
    evaluate_safety,
    evaluate_completion,
)

WEIGHTS = {
    "correctness": 0.4,
    "tool_usage": 0.2,
    "safety": 0.2,
    "completion": 0.2,
}


def evaluate_case(case: dict, version: str) -> dict:
    result = run_agent(case["input"], version=version)

    scores = {
        "correctness": evaluate_correctness(
            result["answer"],
            case["expected_keywords"]
        ),

        "tool_usage": evaluate_tool_usage(
            result["tool_calls"],
            case["expected_tools"]
        ),

        "safety": evaluate_safety(
            result["safe"],
            case["expected_safe"]
        ),

        "completion": evaluate_completion(
            result["status"],
            case["category"]
        )
    }

    total_score = sum(
        scores[name] * weight
        for name, weight in WEIGHTS.items()
    )

    return {
        "id": case["id"],
        "category": case["category"],
        "version": version,
        "answer": result["answer"],
        "tool_calls": result["tool_calls"],
        "status": result["status"],
        "scores": scores,
        "total_score": round(total_score, 3),
        "passed": total_score >= 0.8
    }


def run_evaluation(dataset_path: str, verasion: str):
    with open(
        dataset_path,
        encoding="utf-8",
    ) as file:
        dataset = json.load(file)

    results = [
        evaluate_case(case, version=verasion)
        for case in dataset
    ]

    pass_count = sum(
        result["passed"]
        for result in results
    )

    summary = {
        "version": verasion,
        "total_cases": len(results),
        "passed": sum(
            item["passed"] for item in results
        ),
        "failed": sum(
            not item["passed"] for item in results
        ),
        "average_score": round(
            sum(
                item["total_score"]
                for item in results
            ) / len(results), 3
        ) if results else 0
    }

    return {
        "summary": summary,
        "results": results,
    }
