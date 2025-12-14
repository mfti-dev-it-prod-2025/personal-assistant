"""
Repository for events.
"""

import uuid
from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound

from personal_assistant.src.models.event import Event


class EventRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, event_id: int, user_id: uuid.UUID) -> Event:
        """Получить событие по ID и пользователю."""
        result = await self.session.execute(
            select(Event).where(Event.id == event_id, Event.user_id == user_id)
        )
        event = result.scalars().first()
        if not event:
            raise NoResultFound()
        return event

    async def get_all(
        self, user_id: uuid.UUID, offset: int = 0, limit: int = 100
    ) -> List[Event]:
        """Получить список событий пользователя с пагинацией."""
        result = await self.session.execute(
            select(Event).where(Event.user_id == user_id).offset(offset).limit(limit)
        )
        return result.scalars().all()

    async def create(self, event: Event) -> Event:
        """Создать событие."""
        self.session.add(event)
        await self.session.commit()
        await self.session.refresh(event)
        return event

    async def update(self, event: Event, update_data: dict) -> Event:
        """Обновить поля события."""
        for key, value in update_data.items():
            setattr(event, key, value)
        await self.session.commit()
        await self.session.refresh(event)
        return event

    async def delete(self, event: Event) -> None:
        """Удалить событие."""
        await self.session.delete(event)
        await self.session.commit()
