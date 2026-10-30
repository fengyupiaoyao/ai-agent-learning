from decimal import Decimal

import pytest

from app.budget import TokenBudget, BudgetExceeded


def create_budget():
    return TokenBudget(
        input_price_per_million=Decimal("2"),
        output_price_per_million=Decimal("8"),
        max_input_tokens=10_000,
        max_output_tokens=2_000,
        max_total_tokens=12_000,
        max_model_calls=3,
    )


def test_record_usage():
    budget = create_budget()

    budget.record_usage(
        input_tokens=1000,
        output_tokens=500,
    )

    assert budget.usage.input_tokens == 1000
    assert budget.usage.output_tokens == 500
    assert budget.usage.total_tokens == 1500
    assert budget.model_calls == 1


def test_calculate_cost():
    budget = create_budget()

    budget.record_usage(
        input_tokens=10000,
        output_tokens=2000,
    )

    expected = Decimal("0.036")

    assert budget.cost == expected


def test_max_model_calls():
    budget = create_budget()
    budget.model_calls = 3

    with pytest.raises(BudgetExceeded):
        budget.check_before_call(
            estimated_input_tokens=100,
            max_output_tokens=100,
        )


def test_total_token_budget():
    budget = create_budget()

    budget.record_usage(
        input_tokens=9000,
        output_tokens=1000,
    )

    with pytest.raises(BudgetExceeded):
        budget.check_before_call(
            estimated_input_tokens=1000,
            max_output_tokens=2000,
        )


def test_output_limit():
    budget = create_budget()

    with pytest.raises(BudgetExceeded):
        budget.check_before_call(
            estimated_input_tokens=100,
            max_output_tokens=3000,
        )
