import uuid
from enum import Enum
from typing import List, Optional
from pydantic import EmailStr
from sqlmodel import SQLModel, Field, Relationship

from personal_assistant.src.models.base import BaseTable

name_pattern = r"^[А-Я][А-я]+"


class UserRole(Enum):
    administrator = "administrator"
    user = "user"


class UserBase(SQLModel):
    name: str = Field(regex=name_pattern)
    email: EmailStr = Field(unique=True)


class UserTable(UserBase, BaseTable, table=True):
    __tablename__ = "usertable"
    hashed_password: str
    role: UserRole = Field(default=UserRole.user)
    telegram_id: int | None = Field(default=None, unique=True)

    # Обратная связь на расходы
    expenses: List["ExpenseTable"] = Relationship(back_populates="user")