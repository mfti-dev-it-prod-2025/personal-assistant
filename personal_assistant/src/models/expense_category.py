import uuid
from typing import Optional, List
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

if TYPE_CHECKING:
    from .user import UserTable

from .base import BaseTable


class ExpenseCategoryTable(BaseTable, table=True):
    __tablename__ = "expenses_categories"

    name: str = Field(nullable=False, index=True)
    description: str | None = Field(default=None, nullable=True)

    user_id: uuid.UUID = Field(foreign_key="usertable.id", nullable=False)
    user: Optional["UserTable"] = Relationship(back_populates="categories")

    expenses: List["ExpenseTable"] = Relationship(back_populates="category")
