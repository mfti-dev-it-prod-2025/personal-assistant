from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
import uuid


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=2000)


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=2000)
    is_completed: Optional[bool] = None


class TaskResponse(BaseModel):
    id: uuid.UUID
    title: str
    description: Optional[str]
    is_completed: bool
    user_id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)


class TaskListResponse(BaseModel):
    tasks: list[TaskResponse]
    total: int


class TasksStats(BaseModel):
    total: int = Field(..., description="Общее количество задач")
    completed: int = Field(..., description="Количество выполненных задач")
    pending: int = Field(..., description="Количество невыполненных задач")
    completion_rate: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Процент завершения (от 0.0 до 1.0)"
    )