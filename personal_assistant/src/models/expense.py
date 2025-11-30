from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from datetime import date
import uuid

from .base import BaseTable
from .user import UserTable
from .expense_category import ExpenseCategoryTable


class ExpenseTable(BaseTable, table=True):
    __tablename__ = "expenses"

    # Основные поля
    name: str = Field(nullable=False, unique=True)
    amount: float = Field(nullable=False)
    currency: str = Field(default="RUB", nullable=False)

    # UUID foreign keys
    user_id: uuid.UUID = Field(foreign_key="user_table.id", nullable=False)
    category_id: uuid.UUID = Field(foreign_key="expenses_categories.id", nullable=False)

    tag: Optional[str] = None
    shared: bool = Field(default=False, nullable=False)
    date: date = Field(nullable=False)

    # Связи
    user: Optional[UserTable] = Relationship(back_populates="expenses")
    category: Optional["ExpenseCategoryTable"] = Relationship(back_populates="expenses")


    def __repr__(self) -> str:
        return (
            f"Expense(id={self.id}, name={self.name}, amount={self.amount}, "
            f"date={self.date}, shared={self.shared})"
        )