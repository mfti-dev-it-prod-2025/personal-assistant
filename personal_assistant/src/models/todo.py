import uuid
from sqlmodel import Field

from personal_assistant.src.models.base import BaseTable


class Task(BaseTable, table=True):
    __tablename__ = "tasks"

    title: str = Field(min_length=1, max_length=255)
    description: str = Field(default="", max_length=2000)
    is_completed: bool = Field(default=False)

    user_id: uuid.UUID = Field(foreign_key="usertable.id", nullable=False)
