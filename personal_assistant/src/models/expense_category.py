from typing import List
from sqlmodel import SQLModel, Field, Relationship
import uuid
from datetime import datetime

from .base import BaseTable
from .expense import ExpenseTable  # Импорт для связи

class ExpenseCategoryTable(BaseTable, table=True):
    __tablename__ = "expenses_categories"

    name: str = Field(unique=True, nullable=False)
    description: str | None = Field(default=None, nullable=True)

    # Связь с расходами
    expenses: List["ExpenseTable"] = Relationship(back_populates="category")

