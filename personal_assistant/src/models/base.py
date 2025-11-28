import datetime

from sqlmodel import SQLModel, Field
import uuid


class BaseTable(SQLModel):
    id: uuid.UUID | None = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now()
    )
    updated_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(),
        sa_column_kwargs={"onupdate": lambda: datetime.datetime.now()},
    )
