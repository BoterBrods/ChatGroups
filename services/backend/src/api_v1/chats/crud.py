from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result, func
from sqlalchemy.orm import selectinload

from api_v1.auth.schemas import AuthResponse, AuthRequest
from api_v1.chats.schemas import ChatSchema, ChatCreateSchema, ChatUpdateSchema
from core.models import User, Chat
from core.models.db_helper import db_helper



async def get_all_chats(session: AsyncSession):
    stmt = select(Chat).order_by(Chat.id)
    result: Result = await session.execute(stmt)
    chats = result.scalars().all()

    chat_schemas = [
        ChatSchema.model_validate(chat) for chat in chats
    ]

    return chat_schemas


async def get_chat(session: AsyncSession, chat_id: int) -> Chat | None:
    return await session.get(Chat, chat_id)



async def create_chat(session: AsyncSession, chat: ChatCreateSchema) -> Chat:
    chat = Chat(**chat.model_dump())
    stmt = (
        select(func.count())
        .select_from(Chat)
        .where(Chat.subject == chat.subject)
    )
    chat_exists = await session.scalar(stmt)
    if chat_exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Chat already exists",
        )
    session.add(chat)
    await session.commit()
    return chat


async def update_chat(
    chat_in: ChatUpdateSchema,
    session: AsyncSession,
    chat: Chat,
) -> ChatSchema:

    update_data = chat_in.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        if value == "string":
            continue
        setattr(chat, field, value)

    await session.commit()
    await session.refresh(chat)

    return ChatSchema.model_validate(chat)



async def delete_chat(
        session: AsyncSession,
        chat_id: int,
):
    stmt = (
        select(Chat)
        .where(Chat.id == chat_id)
        .options(
        selectinload(Chat.messages),
        )
    )
    chat = (await session.execute(stmt)).scalars().first()

    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Chat is not found"
        )

    await session.delete(chat)
    await session.commit()

    return {
        "status": "success",
        "message": "Чат и его сообщения удалены",
        "hackathon_id": chat_id,
    }


