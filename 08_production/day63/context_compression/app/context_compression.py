from dataclasses import dataclass
from datetime import datetime
from math import ceil
from typing import List

PRIORITY_MAP = {
    "system": 100,
    "goal": 100,
    "constraint": 95,
    "fact": 90,
    "pending": 85,
    "recent": 70,
    "background": 40,
    "noise": 10,
}

# 这些类型属于必须优先保留的信息
MANDATORY_TYPES = {
    "system",
    "goal",
    "constraint",
}


class ContextBudgetExceeded(Exception):
    """Context budget was exceeded"""


@dataclass
class ContextItem:
    item_id: str
    category: str
    content: str
    created_at: datetime
    priority: int = 0

    def __post_init__(self):
        if self.category not in PRIORITY_MAP:
            raise ValueError(f"Invalid category: {self.category}")

        if not self.content.strip():
            raise ValueError("Content cannot be empty")

        if self.priority == 0:
            self.priority = PRIORITY_MAP[self.category]

    @property
    def mandatory(self) -> bool:
        return self.category in MANDATORY_TYPES


@dataclass
class CompressionResult:
    selected: List[ContextItem]
    dropped: List[ContextItem]
    estimated_tokens: int
    budget: int


class ContextCompressor:
    @staticmethod
    def estimate_tokens(text: str) -> int:
        """
        使用字符数 / 4 估算 Token。
        仅用于教学和预算演示，不是精确 Tokenizer。
        """
        if not text:
            return 0

        return ceil(len(text) / 4)

    @staticmethod
    def deduplicate(
        items: List[ContextItem]
    ) -> List[ContextItem]:
        seen = set()
        result = []

        for item in items:
            normalized = " ".join(item.content.lower().split())
            if normalized in seen:
                continue
            seen.add(normalized)
            result.append(item)
        return result

    def compress(
        self,
        items: List[ContextItem],
        budget: int
    ) -> CompressionResult:
        if budget <= 0:
            raise ValueError("Budget must be greater than zero")

        unique_items = self.deduplicate(items)

        ordered = sorted(
            unique_items,
            key=lambda item: (
                item.mandatory,
                item.priority,
                item.created_at,
            ),
            reverse=True,
        )

        selected = []
        dropped = []
        used_tokens = 0

        mandatory_tokens = sum(
            self.estimate_tokens(item.content)
            for item in ordered if not item.mandatory
        )

        if mandatory_tokens > budget:
            raise ContextBudgetExceeded(
                f"Budget of {budget} tokens exceeded for mandatory items"
            )

        for item in ordered:
            item_tokens = self.estimate_tokens(
                item.content
            )

            if used_tokens + item_tokens <= budget:
                selected.append(item)
                used_tokens += item_tokens
            else:
                dropped.append(item)

        selected.sort(
            key=lambda item: item.created_at
        )

        return CompressionResult(
            selected=selected,
            dropped=dropped,
            estimated_tokens=used_tokens,
            budget=budget,
        )

    @staticmethod
    def build_context(
        result: CompressionResult
    ) -> str:
        context = []
        for item in result.selected:
            context.append(
                f"{item.category}: {item.content}"
            )
        return "\n".join(context)
