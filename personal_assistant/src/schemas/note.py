import uuid
from datetime import datetime

from sqlmodel import SQLModel


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
