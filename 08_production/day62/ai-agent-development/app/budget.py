from dataclasses import dataclass, field
from decimal import Decimal


class BudgetExceeded(Exception):
    """Budget was exceeded"""


@dataclass
class TokenUsage:
    input_tokens: int = 0
    output_tokens: int = 0

    @property
    def total_tokens(self) -> int:
        return self.input_tokens + self.output_tokens


@dataclass
class TokenBudget:
    input_price_per_million: Decimal
    output_price_per_million: Decimal

    max_input_tokens: int = 100_000
    max_output_tokens: int = 20_000
    max_total_tokens: int = 120_000
    max_model_calls: int = 10

    usage: TokenUsage = field(default_factory=TokenUsage)
    model_calls: int = 0

    @property
    def cost(self) -> Decimal:
        input_cost = (
            Decimal(self.usage.input_tokens) *
            self.input_price_per_million / Decimal(1_000_000)
        )

        output_cost = (
            Decimal(self.usage.output_tokens) *
            self.output_price_per_million / Decimal(1_000_000)
        )
        return input_cost + output_cost

    def check_before_call(
        self,
        estimated_input_tokens: int,
        max_output_tokens: int,
    ) -> None:
        if self.model_calls >= self.max_model_calls:
            raise BudgetExceeded("Model call budget exceeded")

        if estimated_input_tokens > self.max_input_tokens:
            raise BudgetExceeded("Input token budget exceeded")
        if max_output_tokens > self.max_output_tokens:
            raise BudgetExceeded("Output token budget exceeded")

        estimated_total = (
            self.usage.total_tokens
            + estimated_input_tokens
            + max_output_tokens
        )

        if estimated_total > self.max_total_tokens:
            raise BudgetExceeded("Total token budget exceeded")

    def record_usage(
        self,
        input_tokens: int,
        output_tokens: int,
    ) -> None:
        if input_tokens < 0 or output_tokens < 0:
            raise ValueError("Token usage cannot be negative")

        self.usage.input_tokens += input_tokens
        self.usage.output_tokens += output_tokens
        self.model_calls += 1
