from fastapi import APIRouter
from .auth.views import auth as router_auth
from .websocket.chat import ws as router_chat


router = APIRouter(prefix="/v1")

router.include_router(router_auth, prefix="/auth")
router.include_router(router_chat, prefix='/chat')

