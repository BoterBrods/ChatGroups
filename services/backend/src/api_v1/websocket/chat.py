import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from ConnectionManager import manager


app = FastAPI()



@app.websocket("/ws}")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_to_all(data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.send_to_all("Пользователь покинул чат")
