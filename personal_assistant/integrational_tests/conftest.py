from typing import Generator, Any

import os
import pytest
import pytest_asyncio
from alembic import command
from alembic.config import Config
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.testclient import TestClient
from testcontainers.postgres import PostgresContainer

from personal_assistant.src.configs.app import settings
from personal_assistant.src.main import app
from personal_assistant.src.models.database_session import get_session


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

def run_migrations(revision: str = "head") -> None:
    repo_root = os.path.dirname(os.path.dirname(__file__))  # .../personal_assistant
    alembic_ini_path = os.path.join(repo_root, "src", "alembic.ini")
    alembic_cfg = Config(alembic_ini_path)
    command.upgrade(config=alembic_cfg, revision=revision)


@pytest.fixture
def router_api():
    client = TestClient(app)
    yield client