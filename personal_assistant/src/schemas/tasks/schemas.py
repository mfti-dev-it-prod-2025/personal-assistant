from pydantic import BaseModel, Field, ConfigDict
import uuid


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(None, max_length=2000)


class TaskUpdate(BaseModel):
    title: str | None = Field(min_length=1, max_length=255)
    description: str | None = Field(max_length=2000)
    is_completed: bool = Field(default=False)


class TaskResponse(BaseModel):
    id: uuid.UUID
    title: str
    description: str = Field(default="")
    is_completed: bool
    user_id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)


class TaskListResponse(BaseModel):
    tasks: list[TaskResponse]
    total: int


class TasksStats(BaseModel):
    total: int
    completed: int
    pending: int
    completion_rate: float = Field(
        ge=0.0,
        le=1.0,
        description="Процент завершения (от 0.0 до 1.0)"
    )