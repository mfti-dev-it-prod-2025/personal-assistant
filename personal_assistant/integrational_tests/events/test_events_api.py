import uuid
from datetime import datetime

import pytest
from sqlmodel import select

from personal_assistant.src.models.event import Event
from personal_assistant.src.schemas.event import EventResponse


def api_path(path: str) -> str:
    """Формирует полный путь API с префиксом /api/v1/."""
    return f"/api/v1/{path}"


@pytest.mark.asyncio
async def test_create_event__then_event_exists_in_db(postgres_connection, router_api_user):
    event_data = {
        "title": "Test Note Title",
        "start_time": "2025-12-15T10:00:00"
    }

    response = router_api_user.post("/api/v1/events/", json=event_data)

    assert response.status_code == 201
    created_event_data = response.json()
    created_event = EventResponse.model_validate(created_event_data)
    assert created_event.title == event_data["title"]
    assert created_event.start_time.strftime("%Y-%m-%dT%H:%M:%S") == event_data["start_time"]

    assert isinstance(created_event.id, uuid.UUID)
    assert isinstance(created_event.created_at, datetime)
    assert isinstance(created_event.updated_at, datetime)
    assert isinstance(created_event.user_id, uuid.UUID)

    db_result = await postgres_connection.exec(
        select(Event).where(Event.id == created_event.id)
    )
    db_event = db_result.first()

    assert db_event is not None
    assert db_event.title == event_data["title"]
    assert db_event.start_time.strftime("%Y-%m-%dT%H:%M:%S") == event_data["start_time"]
    assert db_event.created_at is not None
    assert db_event.updated_at is not None


@pytest.mark.asyncio
async def test_list_events__then_return_non_empty_list(postgres_connection, router_api_user):
    event_data = {
        "title": "Test Note Title",
        "start_time": "2025-12-15T10:00:00"
    }

    router_api_user.post("/api/v1/events/", json=event_data)

    list_response = router_api_user.get(api_path("events/"))
    assert list_response.status_code == 200
    events = list_response.json()

    assert len(events) >= 1


@pytest.mark.asyncio
async def test_get_event_by_id__then_return_correct_event(postgres_connection, router_api_user):
    event_data = {
        "title": "Test Note Title",
        "start_time": "2025-12-15T10:00:00"
    }

    response = router_api_user.post("/api/v1/events/", json=event_data)

    assert response.status_code == 201
    created_event_data = response.json()

    get_response = router_api_user.get(api_path(f"events/{created_event_data["id"]}"))
    event = get_response.json()

    assert event["id"] == created_event_data["id"]
    assert event["title"] == event_data["title"]


@pytest.mark.asyncio
async def test_update_event__then_db_reflects_changes(postgres_connection, router_api_user):
    event_data = {
        "title": "Test Note Title",
        "start_time": "2025-12-15T10:00:00"
    }

    response = router_api_user.post("/api/v1/events/", json=event_data)

    assert response.status_code == 201
    created_event_data = response.json()

    update_data = {"title": "Updated Title", "description": "New description", "start_time": "2025-12-15T10:00:00"}
    update_response = router_api_user.put(api_path(f"events/{created_event_data["id"]}"), json=update_data)
    assert update_response.status_code == 200
    updated_event_data = response.json()

    db_result = await postgres_connection.exec(
        select(Event).where(Event.id == updated_event_data["id"])
    )
    db_event = db_result.first()

    assert db_event.title == update_data["title"]
    assert db_event.description == update_data["description"]


@pytest.mark.asyncio
async def test_delete_event__then_event_not_in_db(postgres_connection, router_api_user):
    event_data = {
        "title": "Test Note Title",
        "start_time": "2025-12-15T10:00:00"
    }

    create_response = router_api_user.post("/api/v1/events/", json=event_data)
    event_id = create_response.json()["id"]

    delete_response = router_api_user.delete(api_path(f"events/{event_id}"))
    assert delete_response.status_code == 204

    db_result = await postgres_connection.exec(
        select(Event).where(Event.id == event_id)
    )
    db_event = db_result.first()

    assert db_event is None


@pytest.mark.asyncio
async def test_create_event_missing_required_fields__then_422(postgres_connection, router_api_user):
    event_data = {"start_time": "2025-12-15T10:00:00"}

    create_response = router_api_user.post("/api/v1/events/", json=event_data)

    assert create_response.status_code == 422
    assert "field required" in create_response.text.lower()


@pytest.mark.asyncio
async def test_create_event_invalid_datetime_format__then_422(postgres_connection, router_api_user):
    invalid_data = {"title": "Invalid Date", "start_time": "not-a-date"}
    response = router_api_user.post(api_path("events/"), json=invalid_data)

    assert response.status_code == 422
    assert 'input should be a valid datetime' in response.text.lower()
