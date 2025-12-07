import uuid
from pydantic import BaseModel
from typing import Optional

class ExpenseCategoryCreate(BaseModel):
    name: str
    description: str

class ExpenseCategoryGet(BaseModel):
    id: uuid.UUID
    name: str
    description: str
    created_at: Optional[str]
    updated_at: Optional[str]

class ExpenseCategoryUpdate(BaseModel):
    name: str
    description: str

class ExpenseCategoryResponse(BaseModel):
    id: uuid.UUID
    name: str
    description: str

    class Config:
        from_attributes = True