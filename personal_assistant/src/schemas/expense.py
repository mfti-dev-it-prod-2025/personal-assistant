import uuid
from datetime import date
from typing import Optional

from pydantic import BaseModel
from sqlmodel import SQLModel, Field


class ExpenseCreate(BaseModel):
    name: str
    amount: float
    currency: str = "RUB"
    category_id: uuid.UUID
    tag: Optional[str] = None
    shared: bool = False
    expense_date: date


class ExpenseUpdate(BaseModel):
    name: Optional[str] = None
    amount: Optional[float] = None
    currency: Optional[str] = None
    category_id: Optional[uuid.UUID] = None
    tag: Optional[str] = None
    shared: Optional[bool] = None
    expense_date: Optional[date] = None


class ExpenseResponse(BaseModel):
    id: uuid.UUID
    name: str
    amount: float
    currency: str
    user_id: uuid.UUID
    category_id: uuid.UUID
    tag: Optional[str]
    shared: bool
    expense_date: date

    class Config:
        from_attributes = True


class ExpensesParams(SQLModel):
    category_name: Optional[str] = Field(default=None)

    start_date: Optional[date] = Field(default=None, description="Начальная дата")
    end_date: Optional[date] = Field(default=None, description="Конечная дата")


class ExpenseParams(SQLModel):
    id: Optional[uuid.UUID] = None
    name: Optional[str] = None
