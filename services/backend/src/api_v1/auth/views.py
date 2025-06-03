from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from api_v1.auth.schemas import AuthResponse, AuthRequest
from core.models import User
from core.models.db_helper import db_helper
from .crud import login_user


auth = APIRouter()


@auth.post(
    "/login",
    response_model=AuthResponse,
    status_code=status.HTTP_201_CREATED,
)
async def login_user(
    auth_data: AuthRequest,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    return login_user(auth_data=auth_data, session=session)