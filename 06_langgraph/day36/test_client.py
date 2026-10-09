import asyncio
import json
import httpx


async def main():
    async with httpx.AsyncClient(timeout=None) as client:
        async with client.stream(
            "POST",
            "http://127.0.0.1:8000/chat/stream",
            json={"question": "解释下 RAG"}
        ) as response:
            response.raise_for_status()

            async for line in response.aiter_lines():
                if line.startswith("event: "):
                    event = line[7:]
                elif line.startswith("data: "):
                    data = json.loads(line[6:])
                    if event == "token":
                        print(data["content"])
                    elif event == "done":
                        print("Done")
                    elif event == "error":
                        print(f"Error: {data['message']}")

asyncio.run(main())
