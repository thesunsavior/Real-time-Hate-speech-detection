import httpx
import asyncio


async def receive_chat_stream(video_id: str):
    url = f"http://127.0.0.1:8000/chat/{video_id}"

    async with httpx.AsyncClient() as client:
        async with client.stream("GET", url) as response:
            async for line in response.aiter_lines():
                print(line)
                if line.startswith("data: "):
                    chat_message = line[len("data: "):]
                    print(f"Received: {chat_message}")

if __name__ == "__main__":
    asyncio.run(receive_chat_stream("tGfQYbArQhc"))
