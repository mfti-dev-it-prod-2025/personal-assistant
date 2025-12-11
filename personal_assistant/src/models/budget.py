from typing import Optional, List
from sqlmodel import Field, Relationship
from datetime import date
import uuid

from .base import BaseTable


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

    user: Optional["UserTable"] = Relationship(back_populates="expenses") # type: ignore
    category: Optional["ExpenseCategoryTable"] = Relationship(back_populates="expenses")

    def __repr__(self) -> str:
        return (
            f"Expense(id={self.id}, name={self.name}, amount={self.amount}, "
            f"date={self.expense_date}, shared={self.shared})"
        )


class ExpenseCategoryTable(BaseTable, table=True):
    __tablename__ = "expenses_categories"

    name: str = Field(unique=True, nullable=False)
    description: str | None = Field(default=None, nullable=True)

    expenses: List["ExpenseTable"] = Relationship(back_populates="category")
