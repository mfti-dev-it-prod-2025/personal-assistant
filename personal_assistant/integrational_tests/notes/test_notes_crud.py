import pytest
import uuid

from dateutil.parser import isoparse
from sqlmodel import select
from datetime import datetime, timezone
from personal_assistant.integrational_tests.utils import random_email
from personal_assistant.src.models.note import Note, NoteRead, NoteReadUpdate
from personal_assistant.src.models.user import UserTable


@pytest.mark.asyncio
async def test_create_note__then_note_exists_in_db_and_returned(postgres_connection, router_api_admin):
    
    note_data = {"title": "Test Note Title", "content": "Test Note Content"}

    response = router_api_admin.post("/api/v1/notes/", json=note_data)

    assert response.status_code == 201
    created_note_data = response.json()
    created_note = NoteRead.model_validate(created_note_data)
    assert created_note.title == note_data["title"]
    assert created_note.content == note_data["content"]
    assert isinstance(created_note.id, uuid.UUID)
    assert isinstance(created_note.created_at, datetime)
    assert isinstance(created_note.updated_at, datetime)
    assert isinstance(created_note.user_id, uuid.UUID)

    db_result = await postgres_connection.exec(
        select(Note).where(Note.id == created_note.id)
    )
    db_note = db_result.first()

    assert db_note is not None
    assert db_note.title == note_data["title"]
    assert db_note.content == note_data["content"]
    assert db_note.created_at is not None
    assert db_note.updated_at is not None

@pytest.mark.asyncio
async def test_read_note_by_id__existing_note(postgres_connection, router_api_admin):

    note_data = {"title": "Read Test Note", "content": "Read Test Content"}
    create_response = router_api_admin.post("/api/v1/notes/", json=note_data)
    assert create_response.status_code == 201
    created_note_id = create_response.json()["id"]

    response = router_api_admin.get(f"/api/v1/notes/{created_note_id}")

    assert response.status_code == 200
    retrieved_note_data = response.json()
    retrieved_note = NoteRead.model_validate(retrieved_note_data)
    assert str(retrieved_note.id) == created_note_id
    assert retrieved_note.title == note_data["title"]
    assert retrieved_note.content == note_data["content"]
    assert isinstance(retrieved_note.user_id, uuid.UUID)


@pytest.mark.asyncio
async def test_read_notes_list__includes_created_note(postgres_connection, router_api_admin):

    note_data = {"title": "List Test Note", "content": "List Test Content"}
    create_response = router_api_admin.post("/api/v1/notes/", json=note_data)
    assert create_response.status_code == 201
    created_note_id = create_response.json()["id"]

    response = router_api_admin.get("/api/v1/notes/")

    assert response.status_code == 200
    notes_list_data = response.json()
    found_note = None
    for note_dict in notes_list_data:
        if note_dict["id"] == created_note_id:
            found_note = NoteRead.model_validate(note_dict)
            break

    assert found_note is not None
    assert found_note.title == note_data["title"]
    assert found_note.content == note_data["content"]
    assert isinstance(found_note.id, uuid.UUID)


@pytest.mark.asyncio
async def test_update_note__changes_data_in_db_and_returns_updated(postgres_connection, router_api_admin):

    initial_note_data = {"title": "Initial Title", "content": "Initial Content"}
    create_response = router_api_admin.post("/api/v1/notes/", json=initial_note_data)
    assert create_response.status_code == 201
    note_id = create_response.json()["id"]

    updated_note_data = {"title": "Updated Title", "content": "Updated Content"}

    response = router_api_admin.put(f"/api/v1/notes/{note_id}", json=updated_note_data)

    assert response.status_code == 200
    updated_note_resp_data = response.json()
    updated_note_resp = NoteReadUpdate.model_validate(updated_note_resp_data)
    assert str(updated_note_resp.id) == note_id
    assert updated_note_resp.title == updated_note_data["title"]
    assert updated_note_resp.content == updated_note_data["content"]
    original_created_at_dt = isoparse(create_response.json()["created_at"])  # распознает Z
    assert updated_note_resp.created_at == original_created_at_dt
    assert isinstance(updated_note_resp.updated_at, datetime)

    db_result = await postgres_connection.exec(
        select(Note).where(Note.id == note_id)
    )
    db_note_after_update = db_result.first()

    assert db_note_after_update is not None
    assert db_note_after_update.title == updated_note_data["title"]
    assert db_note_after_update.content == updated_note_data["content"]
    assert isinstance(db_note_after_update.updated_at, datetime)


@pytest.mark.asyncio
async def test_delete_note__removes_from_db_and_get_returns_404(postgres_connection, router_api_admin):
    
    note_data = {"title": "Delete Test Note", "content": "Delete Test Content"}
    create_response = router_api_admin.post("/api/v1/notes/", json=note_data)
    assert create_response.status_code == 201
    note_id_to_delete = create_response.json()["id"]

    response = router_api_admin.delete(f"/api/v1/notes/{note_id_to_delete}")

    assert response.status_code == 204

    db_result = await postgres_connection.exec(
        select(Note).where(Note.id == note_id_to_delete)
    )
    db_note_after_delete = db_result.first()

    assert db_note_after_delete is None

    get_response = router_api_admin.get(f"/api/v1/notes/{note_id_to_delete}")
    assert get_response.status_code == 404