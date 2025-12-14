"""
Router for managing events.
"""

import uuid
from functools import wraps
from typing import Annotated, List

from fastapi import APIRouter, status, Security, Depends, HTTPException
from sqlalchemy.exc import NoResultFound

from personal_assistant.src.api.dependencies import (
    get_current_user_dependency,
    DbSessionDepends,
)
from personal_assistant.src.models import UserTable
from personal_assistant.src.schemas.event import EventCreate, EventUpdate, EventResponse
from personal_assistant.src.services.event_service import EventService
from personal_assistant.src.repositories.event_repository import EventRepository

router = APIRouter()


def handle_not_found(detail: str = "Событие не найдено"):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except NoResultFound:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail=detail
                )

        return wrapper

    return decorator


def get_event_service_instance(session: DbSessionDepends):
    return EventService(EventRepository(session))


event_service_dependency = Annotated[EventService, Depends(get_event_service_instance)]


@router.get(
    "/{event_id}",
    response_model=EventResponse,
    status_code=status.HTTP_200_OK,
    summary="Получить событие по ID",
    description="Возвращает событие, если оно принадлежит текущему пользователю.",
)
@handle_not_found()
async def get_event(
    event_id: uuid.UUID,
    event_service: event_service_dependency,
    current_user: Annotated[
        UserTable, Security(get_current_user_dependency, scopes=["events:read"])
    ],
) -> EventResponse:
    return await event_service.get_by_id(event_id, current_user.id)


@router.get(
    "/",
    response_model=List[EventResponse],
    status_code=status.HTTP_200_OK,
    summary="Получить список событий",
    description="Возвращает пагинированный список событий текущего пользователя.",
)
async def list_events(
    event_service: event_service_dependency,
    current_user: Annotated[
        UserTable, Security(get_current_user_dependency, scopes=["events:read"])
    ],
    offset: int = 0,
    limit: int = 100,
) -> List[EventResponse]:
    return await event_service.get_all(current_user.id, offset=offset, limit=limit)


@router.post(
    "/",
    response_model=EventResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать событие",
    description="Создаёт новое событие для текущего пользователя.",
)
async def create_event(
    event_data: EventCreate,
    event_service: event_service_dependency,
    current_user: Annotated[
        UserTable, Security(get_current_user_dependency, scopes=["events:create"])
    ],
) -> EventResponse:
    return await event_service.create(event_data, current_user.id)


@router.put(
    "/{event_id}",
    response_model=EventResponse,
    status_code=status.HTTP_200_OK,
    summary="Обновить событие",
    description="Обновляет событие, если оно принадлежит текущему пользователю.",
)
@handle_not_found()
async def update_event(
    event_id: uuid.UUID,
    event_data: EventUpdate,
    event_service: event_service_dependency,
    current_user: Annotated[
        UserTable, Security(get_current_user_dependency, scopes=["events:update"])
    ],
) -> EventResponse:
    return await event_service.update(event_id, event_data, current_user.id)


@router.delete(
    "/{event_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить событие",
    description="Удаляет событие, если оно принадлежит текущему пользователю.",
)
@handle_not_found()
async def delete_event(
    event_id: uuid.UUID,
    event_service: event_service_dependency,
    current_user: Annotated[
        UserTable, Security(get_current_user_dependency, scopes=["events:delete"])
    ],
):
    await event_service.delete(event_id, current_user.id)
