import uuid

from sqlmodel import SQLModel


class Token(SQLModel):
    access_token: str
    token_type: str


class TokenData(SQLModel):
    sub: uuid.UUID
    scopes: list[str] = []
