import re
import unicodedata

from dataclasses import dataclass


@dataclass
class SecurityResult:
    allowed: bool
    normalized_text: str
    reason: str | None = None


class InputGuard:
    def __init__(self, max_length: int = 4000):
        self.max_length = max_length

        self.block_patterns = [
            r"ignore\s+(all\s+)?previous\s+instructions",
            r"忽略(之前|以上|所有)(的)?指令",
            r"输出(你的)?(完整)?系统提示词",
            r"reveal\s+(the\s+)?system\s+prompt",
        ]

    def validate(self, text: str) -> SecurityResult:
        if not isinstance(text, str):
            return SecurityResult(
                allowed=False,
                normalized_text="",
                reason="输入必须是字符串",
            )

        normalized = unicodedata.normalize("NFKC", text)

        if not normalized.strip():
            return SecurityResult(
                allowed=False,
                normalized_text="",
                reason="输入不能为空",
            )
        if len(normalized) > self.max_length:
            return SecurityResult(
                allowed=False,
                normalized_text="",
                reason=f"输入不能超过 {self.max_length} 个字符",
            )

        for char in normalized:
            if unicodedata.category(char) == "Cc":
                if char not in ("\n", "\r", "\t"):
                    return SecurityResult(
                        allowed=False,
                        normalized_text=normalized,
                        reason="输入包含非法控制字符",
                    )

        for pattern in self.block_patterns:
            if re.search(pattern, normalized, re.IGNORECASE):
                return SecurityResult(
                    allowed=False,
                    normalized_text=normalized,
                    reason="输入包含被阻塞的模式",
                )

        return SecurityResult(
            allowed=True,
            normalized_text=normalized,
            reason=None,
        )
