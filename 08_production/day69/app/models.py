from dataclasses import dataclass, field
from this import d
from typing import Any


@dataclass
class UserContext:
    user_id: str
    role: str


@dataclass
class ToolCall:
    tool_name: str
    arguments: dict[str, Any] = field(default_factory=dict)


@dataclass
class ToolResult:
    success: bool
    data: Any = None
    error: str | None = None
    requires_approval: bool = False
