import uuid
from enum import Enum

from pydantic import EmailStr
from sqlmodel import SQLModel, Field

name_pattern = r'^[А-Я][А-я]+'


class UserRole(Enum):
    administrator = "administrator"
    user = "user"


class UserBase(SQLModel):
    name: str = Field(regex=name_pattern)
    email: EmailStr
    role: UserRole

class UserTable(UserBase, table=True):
    id: uuid.UUID | None = Field(default=None, primary_key=True)
    hashed_password: str
    telegram_id: int | None = Field(default=None)
