format:
	@echo "formating"
	poetry run ruff format personal_assistant/src

type:
	@echo "check typing"
	poetry run mypy personal_assistant/src

run:
	@echo "start prod server"
	fastapi run personal_assistant/src/main.py

dev:
	@echo "start dev server"
	fastapi dev personal_assistant/src/main.py

mkmigrate:
	@echo "create alembic migrations"
	cd personal_assistant/src && python3 create_migrations.py

migrate:
	@echo "perform alembic migrations"
	cd personal_assistant/src && alembic upgrade head