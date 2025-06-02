from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User, Chat, Message


async def get_user(
    session: AsyncSession,
    username: str,
    variant: int,
):
    user = await session.scalar(
        select(User).where(
            User.username == username,
            User.variant == variant,
        )
    )
    return user


async def get_chat(
    session: AsyncSession,
    chat_id: int,
):
    chat = await session.scalar(select(Chat).where(Chat.id == chat_id))
    return chat

