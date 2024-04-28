import enum
from datetime import datetime
from typing import List

from pydantic import BaseModel
from sqlalchemy.types import String, BigInteger, Enum, DateTime
from sqlmodel import SQLModel, Field as SQLField, Relationship


class Chat(SQLModel, table=True):  # type: ignore
    __tablename__ = "chat"

    id: int | None = SQLField(default=None, primary_key=True, sa_type=BigInteger)
    user_id: int = SQLField(nullable=False, sa_type=BigInteger, foreign_key="users.id")
    name: str = SQLField(nullable=False, sa_type=String)
    description: str | None = SQLField(default=None, nullable=True, sa_type=String)
    created_at: datetime = SQLField(
        default_factory=datetime.utcnow,
        nullable=False,
        sa_type=DateTime
    )

    messages: List["ChatMessage"] = Relationship(sa_relationship_kwargs=dict(cascade="all, delete"))


class ChatCreate(BaseModel):
    name: str
    description: str | None = None


class ChatRead(BaseModel):
    id: int
    name: str
    description: str | None
    created_at: datetime


class Role(str, enum.Enum):
    user = "user"
    assistant = "assistant"


class ChatMessage(SQLModel, table=True):  # type: ignore
    __tablename__ = "chat_message"

    id: int | None = SQLField(default=None, primary_key=True, sa_type=BigInteger)
    chat_id: int = SQLField(nullable=False, sa_type=BigInteger, foreign_key="chat.id")
    role: Role = SQLField(nullable=False, sa_type=Enum(Role))  # type: ignore
    content: str = SQLField(nullable=False, sa_type=String)
    created_at: datetime = SQLField(
        default_factory=datetime.utcnow,
        nullable=False,
        sa_type=DateTime
    )


class ChatMessageCreate(BaseModel):
    role: Role
    content: str


class ChatMessageRead(BaseModel):
    id: int
    role: Role
    content: str
    created_at: datetime
