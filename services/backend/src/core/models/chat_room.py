from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import mapped_column, relationship, Mapped

from .base import Base

if TYPE_CHECKING:
    from .message import Message


class Chat(Base):
    __tablename__ = "chats"

    subject: Mapped[str] = mapped_column(String[40], nullable=False, unique=True)
    messages: Mapped[list["Message"]] = relationship(
        back_populates="chat", cascade="all, delete-orphan"
    )
