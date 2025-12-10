import datetime
import uuid

from sqlalchemy import DateTime
from sqlmodel import SQLModel, Field


class BaseTable(SQLModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(tz=datetime.timezone.utc),
        sa_type=DateTime(timezone=True),
    )
    updated_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(tz=datetime.timezone.utc),
        sa_column_kwargs={
            "onupdate": lambda: datetime.datetime.now(tz=datetime.timezone.utc)
        },
        sa_type=DateTime(timezone=True),
    )
