import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from .ConnectionManager import manager
from api_v1.redis.redis_cient import save_message, get_history

ws = APIRouter()


html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Websocket Demo</title>
           <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">

    </head>
    <body>
    <div class="container mt-3">
        <h1>FastAPI WebSocket Chat</h1>
        <h2>Your ID: <span id="ws-id"></span></h2>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" class="form-control" id="messageText" autocomplete="off"/>
            <button class="btn btn-outline-primary mt-2">Send</button>
        </form>
        <ul id='messages' class="mt-5">
        </ul>

    </div>

        <script>
            var client_id = Date.now()
            document.querySelector("#ws-id").textContent = client_id;
            const ws = new WebSocket(`ws://${location.host}/api/v1/chat/ws/${client_id}`);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@ws.get("/")
async def get():
    return HTMLResponse(html)

@ws.websocket("/ws/{subject}/{client_id}")
async def websocket_subject_chat(websocket: WebSocket, subject: str, client_id: int):
    await manager.connect(websocket,subject)

    history = await get_history(subject)
    for old_msg in history:
        await manager.send_personal_message(f"[HISTORY] {old_msg}", websocket)

    try:
        while True:
            data = await websocket.receive_text()
            formatted = f"{client_id} @ {subject}: {data}"
            await save_message(subject, formatted)
            await manager.send_to_room(subject,formatted)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.send_to_room(subject,f"{client_id} покинул чат {subject}")