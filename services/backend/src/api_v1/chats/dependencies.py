from pathlib import Path
from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from .crud import get_chat
from core.models import db_helper, Chat
from .schemas import ChatSchema


async def get_chat_by_id(
    chat_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.session_getter),
) -> Chat:
    chat = await get_chat(session=session, chat_id=chat_id)
    if not chat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found")
    return chat
