import asyncio
import os

import uvicorn
from alembic import command
from alembic.config import Config

from personal_assistant.src.configs.app import settings


async def start_server():
    """
    Запускает uvicorn сервер асинхронно.
    """
    config = uvicorn.Config(
        "personal_assistant.src.main:app",
        host=settings.app.app_host,
        port=settings.app.app_port,
        log_level="info",
    )
    server = uvicorn.Server(config)
    await server.serve()


def run_migrations():
    """
    Выполняет миграции базы данных до последней версии (heads).
    """
    base_path = os.path.dirname(__file__)
    alembic_cfg = Config(os.path.join(base_path, "alembic.ini"))
    command.upgrade(alembic_cfg, "heads")


def main():
    asyncio.run(start_server())


if __name__ == "__main__":
    main()
