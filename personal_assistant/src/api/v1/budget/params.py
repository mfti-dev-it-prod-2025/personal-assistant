import uuid

from pydantic import Field, EmailStr, validator
from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel


class ExpensesParams(SQLModel):
    category_name: str | None = Field(default=None)

    start_date: Optional[str] = Field(
        default=None, description="Начальная дата в формате YYYY-MM-DD"
    )
    end_date: Optional[str] = Field(
        default=None, description="Конечная дата в формате YYYY-MM-DD"
    )

    @validator("start_date", "end_date")
    def validate_date(cls, v):
        if v is None:
            return v
        try:
            datetime.strptime(v, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Дата должна быть в формате YYYY-MM-DD")
        return v

    @validator("end_date")
    def validate_start_before_end(cls, v, values):
        if v and values.get("start_date"):
            sd = datetime.strptime(values["start_date"], "%Y-%m-%d")
            ed = datetime.strptime(v, "%Y-%m-%d")
            if ed < sd:
                raise ValueError("Конечная дата не может быть раньше начальной")
        return v


class ExpenseParams(SQLModel):
    id: uuid.UUID | None = None
    name: str | None = None


class ExpenseCategoryParams(SQLModel):
    id: uuid.UUID | None = None
    name: str | None = None
