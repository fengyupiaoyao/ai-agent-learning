import asyncio
import json
import httpx


async def ask(client, question, thread_id):
    print(f"\n用户:{question}")
    print("Agent: ", end="", flush=True)

    async with client.stream(
        "POST",
        "http://127.0.0.1:8000/chat/stream",
        json={"question": question, "thread_id": thread_id},
    ) as response:
        response.raise_for_status()

        current_event = None

        async for line in response.aiter_lines():
            if line.startswith("event: "):
                current_event = line[7:]
            elif line.startswith("data: "):
                data = json.loads(line[6:])
                if current_event == "token":
                    print(data["content"], end="", flush=True)
                elif current_event == "done":
                    print("Done")
                elif current_event == "error":
                    print(f"Error: {data['message']}")


async def main():
    async with httpx.AsyncClient(timeout=None) as client:
        thread_id = "user-001"
        await ask(
            client,
            "我叫小明，正在学习langgraph",
            thread_id
        )

        await ask(
            client,
            "我叫什么？我正在学习什么？",
            thread_id
        )

        await ask(
            client,
            "我叫什么？我正在学习什么？",
            "user-002"
        )

asyncio.run(main())
