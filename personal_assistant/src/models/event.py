from datetime import datetime
from sqlmodel import Field
import uuid


from personal_assistant.src.models.base import BaseTable


class Event(BaseTable, table=True):
    __tablename__ = "events"

    title: str = Field(nullable=False)
    description: str | None
    start_time: datetime = Field(nullable=False)
    end_time: datetime

    user_id: uuid.UUID = Field(foreign_key="usertable.id", nullable=False)
