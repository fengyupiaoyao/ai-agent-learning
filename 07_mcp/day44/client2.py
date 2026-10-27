import anyio
from pathlib import Path

from mcp_service import ResearchMCPClient


async def main():
    server_path = Path(__file__).with_name("server.py")

    async with ResearchMCPClient(server_path) as mcp:
        tools = await mcp.list_tools()
        print([tool.name for tool in tools])

        result = await mcp.search_notes("mcp")
        print(result.content)

if __name__ == "__main__":
    anyio.run(main)
