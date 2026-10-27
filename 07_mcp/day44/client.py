import anyio
import sys
from pathlib import Path

from mcp import Client, StdioServerParameters
from mcp.types import TextContent, TextResourceContents

SERVER_PATH = Path(__file__).with_name("server.py")

async def main():
    server = StdioServerParameters(
        command=sys.executable,
        args=[str(SERVER_PATH)],
    )

    async with Client(server) as client:
        print("Server:", client.server_info)
        print("Protocol:", client.protocol_version)
        print("Capabilities:", client.server_capabilities)

        tools = await client.list_tools()

        print("\n Tools:", tools)
        for tool in tools.tools:
            print(f"\nName: {tool.name}")
            print(f"Description: {tool.description}")
            print(f"Input schema: {tool.input_schema}")
        
        print("\n=== Call Tool ===")
        result = await client.call_tool(
            "search_notes",
            {"keyword": "MCP"},
        )

        if result.is_error:
            print("Tool failed:", result.content)
        else:
            for item in result.content:
                if isinstance(item, TextContent):
                    print(item.text)

            if result.structured_content is not None:
                print("Structured:", result.structured_content)

        # 4. 发现并读取 Resource
        print("\n=== Resources ===")
        resources = await client.list_resources()

        for resource in resources.resources:
            print(resource.uri)

        resource_result = await client.read_resource(
            "research://topics"
        )

        for item in resource_result.contents:
            if isinstance(item, TextResourceContents):
                print(item.text)

        # 5. 发现并获取 Prompt
        print("\n=== Prompts ===")
        prompts = await client.list_prompts()

        for prompt in prompts.prompts:
            print(prompt.name, prompt.arguments)

        prompt_result = await client.get_prompt(
            "create_research_prompt",
            {"topic": "LangGraph"},
        )

        for message in prompt_result.messages:
            print(message.role, message.content)

if __name__ == "__main__":
    anyio.run(main)


