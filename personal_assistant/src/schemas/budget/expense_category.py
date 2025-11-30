import uuid
from pydantic import BaseModel
from typing import Optional

class ExpenseCategoryCreate(BaseModel):
    name: str
    description: float

class ExpenseCategoryGet(BaseModel):
    id: uuid.UUID
    name: str
    description: float
    created_at: Optional[str]
    updated_at: Optional[str]

class ExpenseCategoryUpdate(BaseModel):
    name: str
    description: float