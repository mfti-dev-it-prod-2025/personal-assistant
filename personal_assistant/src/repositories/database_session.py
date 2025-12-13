from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker

from personal_assistant.src.configs.app import settings


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    engine = create_async_engine(url=settings.db.dsl, echo=True, future=True)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    try:
        async with async_session() as session:
            yield session
    finally:
        await engine.dispose()
