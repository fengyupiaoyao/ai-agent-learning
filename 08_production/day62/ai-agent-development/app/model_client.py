from app.budget import TokenBudget


async def invoke_with_budget(
    model,
    messages,
    budget: TokenBudget,
    estimated_input_tokens: int,
    max_output_tokens: int,
):
    budget.check_before_call(
        estimated_input_tokens=estimated_input_tokens,
        max_output_tokens=max_output_tokens,
    )

    response = await model.ainvoke(messages)

    usage = response.usage_metadata or {}

    input_tokens = usage.get("input_tokens", 0)
    output_tokens = usage.get("output_tokens", 0)

    budget.record_usage(
        input_tokens=input_tokens,
        output_tokens=output_tokens,
    )

    return response
