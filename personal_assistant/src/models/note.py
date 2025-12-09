from sqlmodel import Field
import uuid
from personal_assistant.src.models.base import BaseTable


class Note(BaseTable, table=True):
    title: str = Field(index=True)
    content: str

    user_id: uuid.UUID = Field(foreign_key="usertable.id", index=True)
