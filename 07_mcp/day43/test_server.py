import pytest

from mcp import Client

from servers import mcp


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.mark.anyio
async def test_search_notes():
    async with Client(mcp) as client:
        result = await client.call_tool(
            "search_notes",
            {"keyword": "MCP"}
        )

        assert not result.is_error
        assert result.content
        assert "MCP" in str(result.content)


@pytest.mark.anyio
async def test_empty_keyword():
    async with Client(mcp) as client:
        result = await client.call_tool(
            "search_notes",
            {"keyword": ""},
        )

        assert result.is_error
