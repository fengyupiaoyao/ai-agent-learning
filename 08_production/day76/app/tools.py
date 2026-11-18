from dataclasses import dataclass
from enum import Enum
from typing import Callable, Any


class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class ToolDefinition:
    name: str
    risk_level: RiskLevel
    handler: Callable[..., Any]


def search_web(query: str):
    return f"Search result for: {query}"


def read_file(path: str):
    return f"Reading file: {path}"


def delete_file(path: str):
    return f"DELETE: {path}"


TOOLS = {
    "search_web": ToolDefinition(
        name="search_web",
        risk_level=RiskLevel.LOW,
        handler=search_web,
    ),

    "read_file": ToolDefinition(
        name="read_file",
        risk_level=RiskLevel.LOW,
        handler=read_file,
    ),

    "delete_file": ToolDefinition(
        name="delete_file",
        risk_level=RiskLevel.HIGH,
        handler=delete_file,
    ),
}
