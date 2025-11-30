from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone
import uuid

class Note(SQLModel, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(index=True)
    content: str
    created_at: datetime = Field(default_factory=lambda: datetime.utcnow())
    updated_at: datetime = Field(default_factory=lambda: datetime.utcnow())

    user_id: uuid.UUID = Field(foreign_key="usertable.id", index=True)

class NoteCreate(SQLModel):
    title: str
    content: str

class NoteUpdate(SQLModel):
    title: Optional[str] = None
    content: Optional[str] = None

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