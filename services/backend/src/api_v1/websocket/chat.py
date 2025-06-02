import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlalchemy import select
from api_v1.redis.pubsub import publish_message
from core.models import db_helper, User, Chat, Message
from .ConnectionManager import manager
from api_v1.redis.redis_client import save_message, get_history
from .crud import get_user, get_chat

ws = APIRouter()


@ws.websocket("/ws/{chat_id}")
async def websocket_subject_chat(
    websocket: WebSocket,
    chat_id: int,
):
    await manager.connect(websocket, chat_id)

    try:
        history = await get_history(chat_id, limit=20)
        for item in history:
            await websocket.send_text(item)

        async with db_helper.session_factory as session:
            while True:
                data = await websocket.receive_json()
                username = data["username"]
                variant = data["variant"]
                content = data["content"]

                user = await get_user(
                    session=session,
                    username=username,
                    variant=variant,
                )

                if not user:
                    await websocket.send_text(
                        json.dumps({"error": "Пользователь не найден"})
                    )
                    continue

                chat = await get_chat(
                    session=session,
                    chat_id=chat_id,
                )

                if not chat:
                    await websocket.send_text(json.dumps({"error": "Чат не найден"}))
                    continue

                message = Message(
                    content=content,
                    user_id=user.id,
                    chat_id=chat.id,
                )
                session.add(message)
                await session.commit()
                await session.refresh(message)

                message_dict = {
                    "username": user.username,
                    "variant": user.variant,
                    "content": message.content,
                    "timestamp": message.timestamp.isoformat(),
                }
                message_json = json.dumps(message_dict)

                await save_message(chat_id, message_json)

                await publish_message(chat_id, message_dict)
    except WebSocketDisconnect:
        manager.disconnect(websocket, chat_id)
