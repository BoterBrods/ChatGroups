from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


from api_v1.auth.schemas import AuthResponse, AuthRequest
from core.models import User
from core.models.db_helper import db_helper


async def login_user(
    session: AsyncSession,
    auth_data: AuthRequest,
):
    user = await session.scalar(
        select(User).where(
            User.username == auth_data.username,
            User.variant == auth_data.variant,
        )
    )

    if not user:
        user = User(**auth_data.model_dump())
        session.add(user)
        await session.commit()
        await session.refresh(user)

    else:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists",
        )

    return AuthResponse(
        id=user.id,
        name=user.username,
        variant_number=user.variant,
    )
