from agent import run_agent

questions = [
    # "计算 123 + 456",
    # "计算 20 * 30",
    # "计算 100 / 4",
    # "计算 100 / 0",
    "先计算 20 + 30，然后把结果乘以 5。"
]

for question in questions:
    print(f"Question: {question}")
    result = run_agent(question)
    print(f"Result: {result}")
    print("=" * 20)
