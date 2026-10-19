from atexit import register
from typing import Callable, Any


class CapabilityRegistry:
    def __init__(self):
        self._tools: dict[str, Callable[..., Any]] = {}

    def register(self, name: str, fn: Callable[..., Any]):
        self._tools[name] = fn

    def list_tools(self) -> list[str]:
        return sorted(self._tools.keys())

    def call_tool(self, name: str, **kwargs) -> Any:
        if name not in self._tools:
            raise ValueError(f"Tool '{name}' not found")
        return self._tools[name](**kwargs)


def add(a: int, b: int) -> int:
    return a + b


def multiply(a: int, b: int) -> int:
    return a * b


if __name__ == "__main__":
    registry = CapabilityRegistry()

    registry.register("add", add)
    registry.register("multiply", multiply)

    print(registry.list_tools())
    print(registry.call_tool("add", a=1, b=2))
    print(registry.call_tool("multiply", a=3, b=4))
