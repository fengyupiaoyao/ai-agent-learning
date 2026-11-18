from app.tools import TOOLS
from app.executor import SafeToolExecutor

executor = SafeToolExecutor()

result = executor.execute(
    TOOLS["search_web"],
    {"query": "LangGraph Agent"}
)

print(result)

result = executor.execute(
    TOOLS["delete_file"],
    {
        "path": "temp.txt"
    }
)

print(result)
