format:
	@echo "formating"
	poetry run ruff format personal_assistant/src

type:
	@echo "check typing"
	poetry run mypy personal_assistant/src
