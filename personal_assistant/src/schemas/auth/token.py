import uuid

from sqlmodel import SQLModel

from personal_assistant.src.models.user import UserRole


class Token(SQLModel):
    access_token: str
    token_type: str

class TokenData(SQLModel):
    id: uuid.UUID
    telegram_id: int | None
    role: UserRole
