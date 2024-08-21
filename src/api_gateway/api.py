from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import websockets

from config import Config

app = FastAPI()
config = Config()


@app.websocket("/hate-classification/{video_id}")
async def hate_classification(websocket: WebSocket, video_id: str):
    async with websockets.connect(f"ws://{config.CLASSIFICATION_SERVICE_URL}/ws/{video_id}") as ws_service:
        await websocket.accept()
        try:
            while True:
                # Receive the response from the service
                service_response = await ws_service.recv()

                # Send the response back to the client
                await websocket.send_text(service_response)
        except WebSocketDisconnect:
            print(f"Client disconnected")


@app.websocket("/span-tagging/{comment_id}")
def storage(comment_id: str):
    pass
