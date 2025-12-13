import random
from datetime import date
from uuid import uuid4

import pytest_asyncio

from personal_assistant.src.repositories.user import UserRepository
from personal_assistant.src.schemas.user import UserParams


@pytest_asyncio.fixture
async def router_api_category(postgres_connection, router_api_user):
    category_name = f"Тест-{uuid4().hex[:6]}"
    payload = {
        "name": category_name,
        "description": "Тестовая категория"
    }

    user_repository = UserRepository(db_session=postgres_connection)
    user_email = "user@test.ru"
    user_list = await user_repository.get_users(params=UserParams(email=user_email))
    if not user_list:
        raise Exception("User for category creation not found")

    resp = router_api_user.post("/api/v1/expense/category/", json=payload)
    resp.raise_for_status()

    resp.raise_for_status()
    category_data = resp.json()

    yield category_data


@pytest_asyncio.fixture
async def router_api_expense(router_api_user, router_api_category, postgres_connection):
    random_suffix = random.randint(1, 99999)
    category_name = f"Тест-{random_suffix}"
    payload = {
        "amount": 99.9,
        "currency": "RUB",
        "category_id": router_api_category["id"],
        "name": category_name,
        "shared": False,
        "expense_date": date.today().isoformat(),
    }

    resp = router_api_user.post("/api/v1/expense/", json=payload)

    resp.raise_for_status()
    yield resp.json()