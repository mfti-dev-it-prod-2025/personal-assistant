import pytest
from sqlmodel import select

from personal_assistant.src.models import UserTable

@pytest.mark.asyncio
async def test_create_user__then_user_exist_in_db(postgres_connection, router_api):

    response = router_api.post("/api/v1/auth/user/", json={"name": "test_user",
                                        "email": "test@test.ru",
                                        "password": "test"})

    response.raise_for_status()
    print(f"Response: {response.json()}")

    db_result = await postgres_connection.exec(select(UserTable).where(UserTable.id == response.json()["id"]))
    db_result = db_result.one()

    assert str(db_result.id) == response.json()["id"]
    assert db_result.name == response.json()["name"]
    assert db_result.email == response.json()["email"]
    assert db_result.hashed_password

