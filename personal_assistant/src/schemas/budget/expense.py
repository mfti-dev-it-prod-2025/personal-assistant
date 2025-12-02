import uuid
from datetime import date
from pydantic import BaseModel
from typing import Optional

class ExpenseCreate(BaseModel):
    name: str
    amount: float
    currency: str = "RUB"
    user_id: uuid.UUID
    category_id: uuid.UUID
    tag: Optional[str] = None
    shared: bool = False
    expense_date: date

class ExpenseGet(BaseModel):
    id: uuid.UUID
    name: str
    amount: float
    currency: str
    user_id: uuid.UUID
    category_id: uuid.UUID
    tag: Optional[str]
    shared: bool
    date: date
    created_at: Optional[str]
    expense_date: Optional[str]

class ExpenseUpdate(BaseModel):
    name: Optional[str] = None
    amount: Optional[float] = None
    currency: Optional[str] = None
    user_id: Optional[uuid.UUID] = None
    category_id: Optional[uuid.UUID] = None
    tag: Optional[str] = None
    shared: Optional[bool] = None
    expense_date: Optional[date] = None

class ExpenseResponse(BaseModel):
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