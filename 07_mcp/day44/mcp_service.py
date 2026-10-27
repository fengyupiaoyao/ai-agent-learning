import sys
from pathlib import Path

from mcp import Client, StdioServerParameters


class ResearchMCPClient:
    def __init__(self, server_path: str):
        self.server = StdioServerParameters(
            command=sys.executable,
            args=[str(server_path)],
        )
        self.client = None

    async def __aenter__(self):
        self.client = Client(self.server)
        await self.client.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self.client is not None:
            await self.client.__aexit__(exc_type, exc, tb)

    async def list_tools(self):
        if self.client is None:
            raise RuntimeError("Client is not initialized")

        result = await self.client.list_tools()
        return result.tools

    async def search_notes(self, keyword: str):
        if self.client is None:
            raise RuntimeError("Client is not connected")

        return await self.client.call_tool(
            "search_notes",
            {"keyword": keyword},
        )
