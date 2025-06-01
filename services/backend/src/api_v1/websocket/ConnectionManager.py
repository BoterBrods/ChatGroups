from fastapi import WebSocket
from collections import defaultdict

class ConnectionManager:
    def __init__(self):
        self.rooms: dict[str, list[WebSocket]] = defaultdict(list)

    async def connect(self, websocket: WebSocket, subject: str):
        await websocket.accept()
        self.rooms[subject].append(websocket)

    def disconnect(self, websocket: WebSocket):
        for subject, connections in self.rooms.items():
            if websocket in connections:
                connections.remove(websocket)
                break

    async def send_to_room(self, subject: str, message: str):
        for connection in self.rooms.get(subject, []):
            await connection.send_text(message)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)


manager = ConnectionManager()