from datetime import datetime
from typing import Optional, Any
from pydantic import BaseModel, Field, ConfigDict
import uuid


# Схема для создания задачи (без id и временных меток)
class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=2000)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Купить молоко",
                "description": "2.5%, 1 литр"
            }
        }
    )


# Схема для обновления задачи (все поля опциональны)
class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=2000)
    is_completed: Optional[bool] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Купить молоко и хлеб",
                "is_completed": True
            }
        }
    )


# Схема для ответа (все поля, включая системные)
class TaskResponse(BaseModel):
    id: uuid.UUID
    title: str
    description: Optional[str]
    is_completed: bool
    user_id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = ConfigDict(
        from_attributes=True,  # Для работы с ORM-объектами
        json_schema_extra={
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "title": "Купить молоко",
                "description": "2.5%, 1 литр",
                "is_completed": False,
                "user_id": "123e4567-e89b-12d3-a456-426614174001",
                "created_at": "2024-01-01T12:00:00Z",
                "updated_at": "2024-01-01T12:00:00Z"
            }
        }
    )


# Дополнительная схема для списка задач
class TaskListResponse(BaseModel):
    tasks: list[TaskResponse]
    total: int