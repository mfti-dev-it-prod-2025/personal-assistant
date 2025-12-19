import uuid
from typing import Optional

from pydantic import BaseModel
from sqlmodel import SQLModel


class ExpenseCategoryCreate(BaseModel):
    name: str
    description: str


class ExpenseCategoryUpdate(BaseModel):
    name: str | None = None
    description: str | None = None


class ExpenseCategoryResponse(BaseModel):
    id: uuid.UUID
    name: str
    description: str

    class Config:
        from_attributes = True


class ExpenseCategoryParams(SQLModel):
    id: Optional[uuid.UUID] = None
    name: Optional[str] = None
