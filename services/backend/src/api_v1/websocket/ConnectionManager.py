from fastapi import WebSocket
from collections import defaultdict


class ConnectionManager:
    def __init__(self):
        self.rooms: dict[int, list[WebSocket]] = defaultdict(list)

    async def connect(self, websocket: WebSocket, chat_id: int):
        await websocket.accept()
        self.rooms[chat_id].append(websocket)
        print(f"[WebSocket] Пользователь подключён к чату {chat_id} | Всего в комнате: {len(self.rooms[chat_id])}")

    async def disconnect(self, websocket: WebSocket, chat_id: int):
        connections = self.rooms.get(chat_id, [])
        if websocket in connections:
            connections.remove(websocket)
            print(f"[WebSocket] Пользователь отключён от чата {chat_id} | Осталось: {len(connections)}")



    async def send_to_room(self, chat_id: int, message: str):
        for connection in self.rooms.get(chat_id, []):
            await connection.send_text(message)


manager = ConnectionManager()
