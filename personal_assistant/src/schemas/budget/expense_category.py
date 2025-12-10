import uuid
from pydantic import BaseModel

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