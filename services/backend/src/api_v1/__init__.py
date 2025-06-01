from fastapi import APIRouter

from .auth.views import auth as router_auth


router = APIRouter(prefix="/v1")

router.include_router(router_auth, prefix="/auth")
