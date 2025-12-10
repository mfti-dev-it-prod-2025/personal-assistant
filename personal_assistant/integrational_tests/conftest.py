from typing import Generator, Any

import os
import pytest
import pytest_asyncio
from alembic import command
from alembic.config import Config
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette.testclient import TestClient
from testcontainers.postgres import PostgresContainer
from uuid import uuid4
from datetime import date

from personal_assistant.src.api.v1.user.params import UserParams
from personal_assistant.src.configs.app import settings
from personal_assistant.src.main import app
from personal_assistant.src.models.database_session import get_session
from personal_assistant.src.models.user import UserRole
from personal_assistant.src.repositories.user import UserRepository
from personal_assistant.src.schemas.auth.user import UserCreate
from personal_assistant.src.models.budget import ExpenseCategoryTable

@pytest.fixture(scope="session", autouse=True)
def _bootstrap_db() -> Generator[None, Any, None]:
    postgres = None
    try:
        if settings.app.app_use_testcontainers:
            postgres = PostgresContainer("postgres:16-alpine")
            postgres.start()
            settings.db.db_name = postgres.dbname
            settings.db.db_port = int(postgres.get_exposed_port(5432))
            settings.db.db_user = postgres.username
            settings.db.db_password = postgres.password
            settings.db.db_host = postgres.get_container_host_ip()

        run_migrations()
        yield
    finally:
        if postgres is not None:
            postgres.stop()


@pytest_asyncio.fixture
async def postgres_connection(_bootstrap_db) -> AsyncSession:
    agen = get_session()
    session = await agen.__anext__()
    try:
        yield session
    finally:
        await agen.aclose()


def run_migrations(revision: str = "heads") -> None:
    repo_root = os.path.dirname(os.path.dirname(__file__))  # .../personal_assistant
    alembic_ini_path = os.path.join(repo_root, "src", "alembic.ini")
    alembic_cfg = Config(alembic_ini_path)
    command.upgrade(config=alembic_cfg, revision=revision)


@pytest.fixture
def router_api():
    client = TestClient(app)
    yield client


@pytest_asyncio.fixture
async def router_api_admin(postgres_connection):
    user_repository = UserRepository(db_session=postgres_connection)
    admin_email = "admin@admin.ru"
    if not await user_repository.get_users(params=UserParams(email=admin_email)):
        created_user = await user_repository.create_user(
            user=UserCreate(name="admin", email=admin_email, password="admin")
        )
        created_user.role = UserRole.administrator
        postgres_connection.add(created_user)
        await postgres_connection.commit()
    client = TestClient(app)
    auth_response = client.post(
        "/api/v1/auth/token",
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "accept": "application/json",
        },
        data={
            "grant_type": "password",
            "username": "admin@admin.ru",
            "password": "admin",
        },
    )
    auth_response.raise_for_status()
    client.headers["Authorization"] = f"Bearer {auth_response.json()['access_token']}"
    yield client


@pytest_asyncio.fixture
async def router_api_user(postgres_connection):
    user_repository = UserRepository(db_session=postgres_connection)
    user_email = "user@test.ru"
    if not await user_repository.get_users(params=UserParams(email=user_email)):
        await user_repository.create_user(
            user=UserCreate(name="user", email=user_email, password="user")
        )
    client = TestClient(app)
    auth_response = client.post(
        "/api/v1/auth/token",
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "accept": "application/json",
        },
        data={
            "grant_type": "password",
            "username": user_email,
            "password": "user",
        },
    )
    auth_response.raise_for_status()
    client.headers["Authorization"] = f"Bearer {auth_response.json()['access_token']}"
    yield client



@pytest_asyncio.fixture
async def router_api_category(router_api_user):
    category_name = "Тест"
    payload = {
        "name": category_name,
        "description": "Тестовая категория"
    }

    resp = router_api_user.post("/api/v1/expense_category/", json=payload)
    print(resp.status_code, resp.text)  # <-- для отладки
    resp.raise_for_status()
    category_data = resp.json()

    yield category_data


@pytest_asyncio.fixture
async def router_api_expense(router_api_user, router_api_category):
    payload = {
        "amount": 99.9,
        "currency": "RUB",
        "category_id": router_api_category["id"],
        "name": "Тест",
        "shared": False,
        "expense_date": date.today().isoformat(),
    }
    resp = router_api_user.post("/api/v1/expense/", json=payload)
    assert resp.status_code == 201
    return resp.json()