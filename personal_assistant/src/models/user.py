import uuid
from enum import Enum

from pydantic import EmailStr
from sqlmodel import SQLModel, Field

name_pattern = r"^[А-Я][А-я]+"


class UserRole(Enum):
    administrator = "administrator"
    user = "user"


class UserBase(SQLModel):
    name: str = Field(regex=name_pattern)
    email: EmailStr = Field(unique=True)


class UserTable(UserBase, table=True):
    id: uuid.UUID | None = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    role: UserRole = Field(default=UserRole.user)
    telegram_id: int | None = Field(default=None, unique=True)
