import pytest
from sqlmodel import select

from personal_assistant.integrational_tests.utils import random_email
from personal_assistant.src.models import UserTable


@pytest.mark.asyncio
async def test_create_user__then_user_exist_in_db(postgres_connection, router_api):
    response = router_api.post(
        "/api/v1/auth/user/",
        json={"name": "test_user", "email": random_email(), "password": "test"},
    )

    response.raise_for_status()

    db_result = await postgres_connection.exec(
        select(UserTable).where(UserTable.id == response.json()["id"])
    )
    db_result = db_result.one()

    assert str(db_result.id) == response.json()["id"]
    assert db_result.name == response.json()["name"]
    assert db_result.email == response.json()["email"]
    assert db_result.hashed_password


@pytest.mark.asyncio
async def test_create_user__then_get_user(postgres_connection, router_api_admin):
    response_post = router_api_admin.post(
        "/api/v1/auth/user/",
        json={"name": "test_user", "email": random_email(), "password": "test"},
    )

    response_post.raise_for_status()

    response_get = router_api_admin.get("/api/v1/auth/user/")
    response_get.raise_for_status()
    found_user = None
    print(f"Response_get = {response_get.json()}")
    for user in response_get.json():
        if user["id"] == response_post.json()["id"]:
            found_user = user

    assert found_user
    assert found_user == response_post.json()
