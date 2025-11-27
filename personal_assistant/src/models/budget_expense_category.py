from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from typing import Any
from sqlalchemy.ext.asyncio import create_async_engine
import asyncio

from personal_assistant.src.models.budget_base import Base, BaseModelMixin


class Category(Base, BaseModelMixin):
    __tablename__ = "expenses_categories"

    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)  # можно nullable=True, если описание опционально

    # Связь с расходами
    expenses = relationship("Expense", back_populates="category")

    def __repr__(self) -> str:
        return f"Category(uuid={self.uuid}, name={self.name}, desc={self.description})"

    def to_dict(self) -> dict[str, Any]:
        return {
            "uuid": self.uuid,
            "name": self.name,
            "description": self.description,
            "created_at": self.create_at,
            "updated_at": self.update_at,
        }


# --- Асинхронное создание таблиц ---
async def create_db():
    engine = create_async_engine(
        "postgresql+asyncpg://user:password@localhost:5432/postgres",
        echo=True,  # видеть SQL запросы
    )

    async with engine.begin() as connection:
        # Раскомментировать для сброса и создания таблиц заново
        # await connection.run_sync(Base.metadata.drop_all)
        # await connection.run_sync(Base.metadata.create_all)
        pass


if __name__ == "__main__":
    asyncio.run(create_db())