from fastapi import WebSocket


class ConnectionManager:
    """Class defining socket events"""

    def __init__(self):
        self.video_active_connections = {}
    
    def add_video(self, video_id: str):
        self.video_active_connections[video_id] = set()

    async def connect(self, websocket: WebSocket, video_id: str):
        await websocket.accept()
        self.video_active_connections[video_id].add(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)
    
    async def broadcast(self, message: str, video_id: str):
        for connection in self.video_active_connections[video_id]:
            await connection.send_text(message)

    def disconnect(self, websocket: WebSocket, video_id: str):
        self.video_active_connections[video_id].remove(websocket)
