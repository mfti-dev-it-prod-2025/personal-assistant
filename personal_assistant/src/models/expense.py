import uuid
from datetime import date
from typing import Optional, TYPE_CHECKING

from sqlmodel import Field, Relationship

from personal_assistant.src.models.base import BaseTable

if TYPE_CHECKING:
    from .expense_category import ExpenseCategoryTable


class ExpenseTable(BaseTable, table=True):
    __tablename__ = "expenses"

    name: str = Field(nullable=False)
    amount: float = Field(nullable=False)
    currency: str = Field(default="RUB", nullable=False)

    user_id: uuid.UUID = Field(foreign_key="usertable.id", nullable=False)
    category_id: uuid.UUID = Field(foreign_key="expenses_categories.id", nullable=False)

    tag: str | None = None
    shared: bool = Field(default=False, nullable=False)
    expense_date: date = Field(nullable=False)

    category: Optional["ExpenseCategoryTable"] = Relationship(back_populates="expenses")
