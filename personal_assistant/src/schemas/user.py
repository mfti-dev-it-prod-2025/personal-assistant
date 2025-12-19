import uuid

from pydantic import BaseModel, EmailStr
from sqlmodel import SQLModel, Field

from personal_assistant.src.models.user import UserRole, name_pattern, UserBase


class UserCreate(UserBase):
    password: str


class UserGet(UserBase):
    id: uuid.UUID
    telegram_id: int | None
    role: UserRole


class UserListResponse(BaseModel):
    result: list[UserGet]
    limit: int
    offset: int
    total: int


class UserParams(SQLModel):
    id: uuid.UUID | None = None
    telegram_id: int | None = None
    role: UserRole | None = None
    email: EmailStr | None = None
    email__contains: str | None = None
    name: str | None = Field(default=None, regex=name_pattern)
    name__contains: str | None = None
    limit: int = 20
    offset: int = 0
