import os

from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel import SQLModel, create_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from sqlalchemy.orm import sessionmaker

from personal_assistant.src.configs.app import settings

DATABASE_URL = os.environ.get("DATABASE_URL")

engine = AsyncEngine(create_engine(url=settings.db.dsl, echo=True, future=True))



async def get_session() -> AsyncSession:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
