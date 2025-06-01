from .websocket.chat import ws as router_chat
from fastapi import APIRouter


router = APIRouter(prefix='/v1')

router.include_router(router_chat, prefix='/chat')