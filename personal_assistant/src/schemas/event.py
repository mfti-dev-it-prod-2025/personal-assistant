"""
Schema for events.
"""

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator


class EventBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: Optional[datetime] = None

    @field_validator("end_time")
    @classmethod
    def validate_time_interval(cls, v, info):
        if v is not None and "start_time" in info.data:
            if v <= info.data["start_time"]:
                raise ValueError("Время окончания должно быть позже времени начала")
        return v


class EventCreate(EventBase):
    pass


class EventUpdate(EventBase):
    pass


class EventResponse(BaseModel):
    id: uuid.UUID
    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: Optional[datetime] = None
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
