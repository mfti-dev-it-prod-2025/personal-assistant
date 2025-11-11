from alembic import command
from alembic.config import Config
from testcontainers.postgres import PostgresContainer

from personal_assistant.src.configs.app import DBConfig, settings


def main():
    postgres = PostgresContainer("postgres:18")
    settings.db.db_name = postgres.dbname
    settings.db.db_port = postgres.port
    settings.db.db_user = postgres.username
    settings.db.db_password = postgres.password
    settings.db.db_host = postgres.get_container_host_ip()

    postgres.start()

    alembic_cfg = Config("alembic.ini")
    command.upgrade(config=alembic_cfg, revision="head")
    upgrade_message = input("Введите описание миграции: ")
    command.revision(config=alembic_cfg, autogenerate=True, message=upgrade_message)

if __name__ == "__main__":
    main()