from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone
import uuid
from personal_assistant.src.models.base import BaseTable

class Note(BaseTable, table=True):
    title: str = Field(index=True)
    content: str
    
    user_id: uuid.UUID = Field(foreign_key="usertable.id", index=True)


class NoteCreate(SQLModel):
    title: str
    content: str

class NoteUpdate(SQLModel):
    title: str | None = None
    content: str | None = None

class NoteRead(SQLModel):
    id: uuid.UUID
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
    user_id: uuid.UUID

class NoteReadUpdate(SQLModel):
    id: uuid.UUID
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
    user_id: uuid.UUID