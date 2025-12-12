import uuid
from typing import Optional
from datetime import date
from sqlmodel import SQLModel, Field


class ExpensesParams(SQLModel):
    category_name: Optional[str] = Field(default=None)

    start_date: Optional[date] = Field(
        default=None, description="Начальная дата"
    )
    end_date: Optional[date] = Field(
        default=None, description="Конечная дата"
    )


class ExpenseParams(SQLModel):
    id: Optional[uuid.UUID] = None
    name: Optional[str] = None


class ExpenseCategoryParams(SQLModel):
    id: Optional[uuid.UUID] = None
    name: Optional[str] = None