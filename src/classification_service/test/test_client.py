import asyncio
import websockets
import json


async def test_websocket(video_id):
    # Replace with your actual server URL
    uri = f"ws://localhost:8000/ws/{video_id}"
    async with websockets.connect(uri) as websocket:
        while True:
            try:
                response = await websocket.recv()
                data = json.loads(response)
                print(f"Received message: {data}")
            except websockets.ConnectionClosed:
                print("Connection closed")
                break

if __name__ == "__main__":
    video_id = "YOUR_VIDEO_ID"  # Replace with the actual video ID you want to test
    asyncio.run(test_websocket(video_id))
