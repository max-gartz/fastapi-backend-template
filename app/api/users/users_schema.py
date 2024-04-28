from typing import List

from pydantic import BaseModel, SecretStr, EmailStr
from sqlalchemy.types import String, BigInteger, Boolean
from sqlmodel import SQLModel, Field as SQLField, Relationship


class User(SQLModel, table=True):  # type: ignore
    __tablename__ = "users"

    id: int | None = SQLField(default=None, primary_key=True, sa_type=BigInteger)
    email: EmailStr = SQLField(index=True, unique=True, sa_type=String)
    name: str = SQLField(nullable=False, sa_type=String)
    password_hash: str = SQLField(nullable=False, sa_type=String)
    is_admin: bool = SQLField(default=False, sa_type=Boolean)

    chats: List["Chat"] = Relationship(sa_relationship_kwargs=dict(cascade="all, delete"))  # type: ignore # noqa: F821


class UserRead(BaseModel):
    id: int
    email: EmailStr
    name: str
    is_admin: bool


class UserCreate(BaseModel):
    email: EmailStr
    name: str
    password: SecretStr


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    name: str | None = None
    password: SecretStr | None = None
