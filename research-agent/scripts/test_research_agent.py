import json

from app.services.research_service import ResearchService

service = ResearchService()

result = service.run(
    question=(
        "研究 LangGraph Checkpoint 机制，"
        "重点分析工作原理、持久化机制和实际应用场景。"
    ),
    user_id="user-123",
    max_steps=4,
)

print("\n========== Research Plan ==========")

for step in result["plan"]:

    print(
        f'{step["step_id"]}: '
        f'{step["task"]}'
    )

    print(
        f'Tool: {step["tool"]}'
    )

    print(
        f'Query: {step["query"]}'
    )

print("\n========== Research Results ==========")

for item in result["results"]:

    print(f'\nStep: {item["step_id"]}')

    print(f'Tool: {item["tool"]}')

    print(f'Result: {item["result"][:1000]}')

print("\n========== Summary ==========")

print(
    json.dumps(
        {
            "status": result["status"],
            "total_steps": result["total_steps"],
        },
        ensure_ascii=False,
        indent=2,
    )
)
