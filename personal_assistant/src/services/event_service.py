"""
Service for events.
"""

import uuid
from typing import List

from personal_assistant.src.models.event import Event
from personal_assistant.src.repositories.event_repository import EventRepository
from personal_assistant.src.schemas.event import EventCreate, EventUpdate, EventResponse


class EventService:
    def __init__(self, repository: EventRepository):
        self.repository = repository

    async def get_by_id(self, event_id: int, user_id: uuid.UUID) -> EventResponse:
        """Получить событие по ID."""
        event = await self.repository.get_by_id(event_id, user_id)
        return EventResponse.model_validate(event, from_attributes=True)

    async def get_all(
        self, user_id: uuid.UUID, offset: int = 0, limit: int = 100
    ) -> List[EventResponse]:
        """Получить список событий пользователя."""
        events = await self.repository.get_all(user_id, offset, limit)
        return [
            EventResponse.model_validate(event, from_attributes=True)
            for event in events
        ]

    async def create(
        self, event_data: EventCreate, user_id: uuid.UUID
    ) -> EventResponse:
        """Создать событие."""
        event = Event(**event_data.model_dump())
        event.user_id = user_id
        event = await self.repository.create(event)
        return EventResponse.model_validate(event, from_attributes=True)

    async def update(
        self, event_id: int, update_data: EventUpdate, user_id: uuid.UUID
    ) -> EventResponse:
        """Обновить событие."""
        event = await self.repository.get_by_id(event_id, user_id)
        update_dict = update_data.model_dump(exclude_unset=True)
        event = await self.repository.update(event, update_dict)
        return EventResponse.model_validate(event, from_attributes=True)

    async def delete(self, event_id: int, user_id: uuid.UUID) -> None:
        """Удалить событие."""
        event = await self.repository.get_by_id(event_id, user_id)
        await self.repository.delete(event)
