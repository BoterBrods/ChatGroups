from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.chats.dependencies import get_chat_by_id
from core.models import Chat
from core.models.db_helper import db_helper
from api_v1.chats.schemas import ChatSchema, ChatCreateSchema, ChatUpdateSchema
from . import crud

router = APIRouter(tags=["Чаты"])


@router.get("/", response_model=list[ChatSchema])
async def get_chats(session: AsyncSession = Depends(db_helper.session_getter)):
    return await crud.get_all_chats(session=session)


@router.get("/{chat_id}", response_model=ChatSchema)
async def get_chat(chat: Chat = Depends(get_chat_by_id)):
    return chat


@router.post("/", response_model=ChatSchema, status_code=201)
async def create_chat(
    chat_in: ChatCreateSchema, session: AsyncSession = Depends(db_helper.session_getter)
):
    return crud.create_chat(session=session, chat=chat_in)


@router.patch("/{chat_id}", response_model=ChatSchema)
async def update_chat(
    chat_in: ChatUpdateSchema,
    chat: Chat = Depends(get_chat_by_id),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    return await crud.update_chat(chat_in=chat_in, session=session, chat=chat)


