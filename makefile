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

create_migration:
	@echo "create alembic migrations"
	python3 personal_assistant/src/alembic/create_migrations.py