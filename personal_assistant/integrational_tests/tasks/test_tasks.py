import uuid

import pytest
from sqlmodel import select

from personal_assistant.src.models.todo import Task


@pytest.mark.asyncio
async def test_create_task__then_task_exists_in_db_and_returned(postgres_connection, router_api_user):
    task_data = {
        "title": "Test Task Title",
        "description": "Test Task Description",
        "is_completed": False
    }

    response = router_api_user.post("/api/v1/tasks/", json=task_data)

    assert response.status_code == 201
    created_task_data = response.json()
    assert created_task_data["title"] == task_data["title"]
    assert created_task_data["description"] == task_data["description"]
    assert created_task_data["is_completed"] == task_data["is_completed"]
    assert isinstance(uuid.UUID(created_task_data["id"]), uuid.UUID)
    assert isinstance(uuid.UUID(created_task_data["user_id"]), uuid.UUID)

    db_result = await postgres_connection.exec(
        select(Task).where(Task.id == uuid.UUID(created_task_data["id"]))
    )
    db_task = db_result.first()

    assert db_task is not None
    assert db_task.title == task_data["title"]
    assert db_task.description == task_data["description"]
    assert db_task.is_completed == task_data["is_completed"]
    assert db_task.created_at is not None
    assert db_task.updated_at is not None


@pytest.mark.asyncio
async def test_read_task_by_id__existing_task(postgres_connection, router_api_user):
    task_data = {"title": "Read Test Task", "description": "Read Test Description"}
    create_response = router_api_user.post("/api/v1/tasks/", json=task_data)
    assert create_response.status_code == 201
    created_task_id = create_response.json()["id"]

    response = router_api_user.get(f"/api/v1/tasks/{created_task_id}")

    assert response.status_code == 200
    retrieved_task_data = response.json()
    assert retrieved_task_data["id"] == created_task_id
    assert retrieved_task_data["title"] == task_data["title"]
    assert retrieved_task_data["description"] == task_data["description"]
    assert isinstance(uuid.UUID(retrieved_task_data["user_id"]), uuid.UUID)


@pytest.mark.asyncio
async def test_read_tasks_list__includes_created_task(postgres_connection, router_api_user):
    task_data = {"title": "List Test Task", "description": "List Test Description"}
    create_response = router_api_user.post("/api/v1/tasks/", json=task_data)
    assert create_response.status_code == 201
    created_task_id = create_response.json()["id"]

    response = router_api_user.get("/api/v1/tasks/")

    assert response.status_code == 200
    tasks_list_data = response.json()

    assert "tasks" in tasks_list_data
    assert "total" in tasks_list_data

    found_task = None
    for task_dict in tasks_list_data["tasks"]:
        if task_dict["id"] == created_task_id:
            found_task = task_dict
            break

    assert found_task is not None
    assert found_task["title"] == task_data["title"]
    assert found_task["description"] == task_data["description"]
    assert isinstance(uuid.UUID(found_task["id"]), uuid.UUID)


@pytest.mark.asyncio
async def test_update_task__changes_data_in_db_and_returns_updated(postgres_connection, router_api_user):
    initial_task_data = {"title": "Initial Title", "description": "Initial Description"}
    create_response = router_api_user.post("/api/v1/tasks/", json=initial_task_data)
    assert create_response.status_code == 201
    task_id = create_response.json()["id"]

    updated_task_data = {"title": "Updated Title", "description": "Updated Description"}

    response = router_api_user.put(f"/api/v1/tasks/{task_id}", json=updated_task_data)

    assert response.status_code == 200
    updated_task_resp_data = response.json()
    assert str(updated_task_resp_data["id"]) == task_id
    assert updated_task_resp_data["title"] == updated_task_data["title"]
    assert updated_task_resp_data["description"] == updated_task_data["description"]

    db_result = await postgres_connection.exec(
        select(Task).where(Task.id == uuid.UUID(task_id))
    )
    db_task_after_update = db_result.first()

    assert db_task_after_update is not None
    assert db_task_after_update.title == updated_task_data["title"]
    assert db_task_after_update.description == updated_task_data["description"]
    assert isinstance(db_task_after_update.updated_at, type(db_task_after_update.created_at))


@pytest.mark.asyncio
async def test_delete_task__removes_from_db_and_get_returns_404(postgres_connection, router_api_user):
    task_data = {"title": "Delete Test Task", "description": "Delete Test Content"}
    create_response = router_api_user.post("/api/v1/tasks/", json=task_data)
    assert create_response.status_code == 201
    task_id_to_delete = create_response.json()["id"]

    response = router_api_user.delete(f"/api/v1/tasks/{task_id_to_delete}")

    assert response.status_code == 204

    db_result = await postgres_connection.exec(
        select(Task).where(Task.id == uuid.UUID(task_id_to_delete))
    )
    db_task_after_delete = db_result.first()

    assert db_task_after_delete is None

    get_response = router_api_user.get(f"/api/v1/tasks/{task_id_to_delete}")
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_mark_task_completed__sets_is_completed_true(postgres_connection, router_api_user):
    task_data = {"title": "Complete Test Task", "description": "Test Description"}
    create_response = router_api_user.post("/api/v1/tasks/", json=task_data)
    assert create_response.status_code == 201
    task_id = create_response.json()["id"]
    assert create_response.json()["is_completed"] is False

    response = router_api_user.put(f"/api/v1/tasks/{task_id}", json={**task_data, "is_completed": True})

    assert response.status_code == 200
    completed_task_data = response.json()
    assert completed_task_data["is_completed"] is True

    db_result = await postgres_connection.exec(
        select(Task).where(Task.id == uuid.UUID(task_id))
    )
    db_task = db_result.first()
    assert db_task is not None
    assert db_task.is_completed is True


@pytest.mark.asyncio
async def test_mark_task_uncompleted__sets_is_completed_false(postgres_connection, router_api_user):
    task_data = {"title": "Uncomplete Test Task", "description": "Test Description"}
    create_response = router_api_user.post("/api/v1/tasks/", json=task_data)
    assert create_response.status_code == 201
    task_id = create_response.json()["id"]

    complete_response = router_api_user.put(f"/api/v1/tasks/{task_id}", json={**task_data, "is_completed": True})
    assert complete_response.status_code == 200
    assert complete_response.json()["is_completed"] is True

    response = router_api_user.put(f"/api/v1/tasks/{task_id}", json={**task_data, "is_completed": False})

    assert response.status_code == 200
    uncompleted_task_data = response.json()
    assert uncompleted_task_data["is_completed"] is False

    db_result = await postgres_connection.exec(
        select(Task).where(Task.id == uuid.UUID(task_id))
    )
    db_task = db_result.first()
    assert db_task is not None
    assert db_task.is_completed is False


@pytest.mark.asyncio
async def test_get_tasks_stats__returns_correct_statistics(postgres_connection, router_api_user):
    task1_data = {"title": "Task 1", "description": "Description 1"}
    task2_data = {"title": "Task 2", "description": "Description 2"}
    task3_data = {"title": "Task 3", "description": "Description 3"}

    create_response1 = router_api_user.post("/api/v1/tasks/", json=task1_data)
    create_response2 = router_api_user.post("/api/v1/tasks/", json=task2_data)
    create_response3 = router_api_user.post("/api/v1/tasks/", json=task3_data)

    assert create_response1.status_code == 201
    assert create_response2.status_code == 201
    assert create_response3.status_code == 201

    task1_id = create_response1.json()["id"]
    task2_id = create_response2.json()["id"]

    complete_response1 = router_api_user.put(f"/api/v1/tasks/{task1_id}", json={**task1_data, "is_completed": True})
    complete_response2 = router_api_user.put(f"/api/v1/tasks/{task2_id}", json={**task2_data, "is_completed": True})

    assert complete_response1.status_code == 200
    assert complete_response2.status_code == 200

    response = router_api_user.get("/api/v1/tasks/stats/me")

    assert response.status_code == 200
    stats_data = response.json()

    assert "total" in stats_data
    assert "completed" in stats_data
    assert "pending" in stats_data
    assert "completion_rate" in stats_data

    assert stats_data["total"] == 3
    assert stats_data["completed"] == 2
    assert stats_data["pending"] == 1
    assert stats_data["completion_rate"] == 2 / 3


@pytest.mark.asyncio
async def test_get_tasks_with_completed_filter__returns_only_completed(postgres_connection, router_api_user):
    task1_data = {"title": "Completed Task", "description": "Description 1"}
    task2_data = {"title": "Pending Task", "description": "Description 2"}

    create_response1 = router_api_user.post("/api/v1/tasks/", json=task1_data)
    create_response1.raise_for_status()
    create_response2 = router_api_user.post("/api/v1/tasks/", json=task2_data)
    create_response2.raise_for_status()

    task1_id = create_response1.json()["id"]
    router_api_user.put(f"/api/v1/tasks/{task1_id}", json={**task1_data, "is_completed": True})

    response_completed = router_api_user.get("/api/v1/tasks/?completed=true")
    response_pending = router_api_user.get("/api/v1/tasks/?completed=false")
    response_all = router_api_user.get("/api/v1/tasks/")

    assert response_completed.status_code == 200
    assert response_pending.status_code == 200
    assert response_all.status_code == 200

    completed_data = response_completed.json()
    pending_data = response_pending.json()
    all_data = response_all.json()

    assert completed_data["total"] == 1
    assert pending_data["total"] == 1
    assert all_data["total"] == 1

    assert len(completed_data["tasks"]) == 1
    assert len(pending_data["tasks"]) == 1
    assert len(all_data["tasks"]) == 1


@pytest.mark.asyncio
async def test_get_tasks_with_pagination__returns_correct_page(postgres_connection, router_api_user):
    for i in range(5):
        task_data = {"title": f"Task {i}", "description": f"Description {i}"}
        router_api_user.post("/api/v1/tasks/", json=task_data)

    response_page1 = router_api_user.get("/api/v1/tasks/?skip=0&limit=2")
    response_page2 = router_api_user.get("/api/v1/tasks/?skip=2&limit=2")
    response_page3 = router_api_user.get("/api/v1/tasks/?skip=4&limit=2")

    assert response_page1.status_code == 200
    assert response_page2.status_code == 200
    assert response_page3.status_code == 200

    page1_data = response_page1.json()
    page2_data = response_page2.json()
    page3_data = response_page3.json()

    assert len(page1_data["tasks"]) == 2
    assert len(page2_data["tasks"]) == 2
    assert len(page3_data["tasks"]) == 1

    assert page1_data["total"] == 5
    assert page2_data["total"] == 5
    assert page3_data["total"] == 5
