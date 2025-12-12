from enum import Enum

from typing import List, TYPE_CHECKING

from pydantic import EmailStr, field_serializer, field_validator
from sqlmodel import SQLModel, Field, Relationship

from personal_assistant.src.models.base import BaseTable
from personal_assistant.src.models.budget import ExpenseTable, ExpenseCategoryTable

if TYPE_CHECKING:
    pass

name_pattern = r"^[А-Я][А-я]+"


class UserRole(Enum):
    administrator = "administrator"
    user = "user"


class UserBase(SQLModel):
    name: str = Field(regex=name_pattern)
    email: EmailStr = Field(unique=True)

    @field_validator("email")
    def normalize_email(cls, v):
        return v.lower() if isinstance(v, str) else v

    @field_serializer("email")
    def serialize_email(self, value: EmailStr, _info):
        return str(value).lower()


class UserTable(UserBase, BaseTable, table=True):
    hashed_password: str
    role: UserRole = Field(default=UserRole.user)
    telegram_id: int | None = Field(default=None, unique=True)
    expenses: List["ExpenseTable"] = Relationship(back_populates="user")
    categories: List["ExpenseCategoryTable"] = Relationship(back_populates="user")

