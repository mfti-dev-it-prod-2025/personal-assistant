ROOT_PATH = personal_assistant/src
format:
	@echo "formating"
	poetry run ruff format $(ROOT_PATH)

type:
	@echo "check typing"
	poetry run mypy $(ROOT_PATH)

run:
	@echo "start prod server"
	fastapi run $(ROOT_PATH)/main.py

dev:
	@echo "start dev server"
	fastapi dev $(ROOT_PATH)/main.py

BRANCH ?= main
mkmigrate:
	@echo "create alembic migrations with label $(BRANCH)"
	cd $(ROOT_PATH) && python3 create_migrations.py --branch-label $(BRANCH)

migrate:
	@echo "perform alembic migrations"
	cd $(ROOT_PATH) && alembic upgrade head

utest:
	@echo "run unit test"
	pytest personal_assistant/
