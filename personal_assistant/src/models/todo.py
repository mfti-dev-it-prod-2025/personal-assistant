import uuid
from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship

from personal_assistant.src.models.base import BaseTable

if TYPE_CHECKING:
    from personal_assistant.src.models.user import UserTable


class Task(BaseTable, table=True):
    __tablename__ = "tasks"

    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=2000)
    is_completed: bool = Field(default=False)

    # Связь с пользователем (один пользователь - много задач)
    user_id: uuid.UUID = Field(foreign_key="usertable.id", nullable=False)
    user: "UserTable" = Relationship(back_populates="tasks")