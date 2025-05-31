from enum import unique
from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.testing.schema import mapped_column
from sqlalchemy.orm import relationship, Mapped
from datetime import datetime


from .base import Base

if TYPE_CHECKING:
    from .message import Message


class User(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(
        String[20], unique=True, nullable=False, index=True
    )
    variant: Mapped[int] = mapped_column(nullable=False)
    messages: Mapped[list["Message"]] = relationship(
        back_populates="author", cascade="all, delete-orphan"
    )
