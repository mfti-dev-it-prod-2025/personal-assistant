import uuid

from personal_assistant.src.models.user import UserBase


class UserCreate(UserBase):
    password: str


class UserGet(UserBase):
    id: uuid.UUID
    telegram_id: int | None
