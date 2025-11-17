# Personal Assistant (FastAPI)

Небольшой сервис на базе FastAPI с аутентификацией (JWT), пользователями и служебными эндпоинтами. Проект использует асинхронный стек (SQLModel + asyncpg), управляет миграциями через Alembic и настраивается через Dynaconf (settings.toml и переменные окружения).

Сервис включает:
- REST API с OpenAPI-документацией (/docs, /redoc)
- OAuth2 Password Flow для получения JWT токена
- Пользовательские эндпоинты с проверкой прав (scopes)
- Health-check


Обзор стека
- Язык: Python 3.12
- Веб-фреймворк: FastAPI
- Модель/ORM: SQLModel (SQLAlchemy)
- БД-драйвер: asyncpg (PostgreSQL)
- Миграции: Alembic
- Конфигурация: Dynaconf + Pydantic-модели
- Запуск сервера: fastapi CLI / uvicorn
- Тесты: pytest, pytest-asyncio, testcontainers (для интеграционных)
- Качество кода: ruff (format), mypy (typing)
- Пакетный менеджер: Poetry
- Контейнеризация: Docker
- CI/CD: GitHub Actions (юнит- и интеграционные тесты, сборка образа)


Точки входа и основные файлы
- Приложение: personal_assistant/src/main.py (объект FastAPI: app)
  - Uvicorn-путь: personal_assistant.src.main:app
- Настройки: settings.toml (в корне репозитория) + переменные окружения (Dynaconf)
- Makefile: основные сценарии разработки/запуска/тестов
- Dockerfile: сборка образа приложения


Требования
- Python 3.12+
- Poetry 2.x
- GNU Make
- PostgreSQL 16+ (локально или через Docker/Testcontainers)
- Опционально: Docker (для контейнерного запуска и/или БД)


Установка
1) Клонировать репозиторий
   git clone <repo_url>
   cd personal-assistant

2) Установить зависимости
   pip install -U poetry
   poetry install

3) Подготовить БД
   - Запустите PostgreSQL локально или через Docker/Compose (см. ниже).
   - Примените миграции:
     make migrate


Запуск
- Режим разработки (автоперезапуск):
  make dev

- Обычный запуск:
  make run

Альтернатива через uvicorn напрямую:
  poetry run uvicorn personal_assistant.src.main:app --host 0.0.0.0 --port 8000

После старта:
- Документация Swagger UI: http://localhost:8000/docs
- Redoc: http://localhost:8000/redoc
- Health-check: GET http://localhost:8000/api/v1/misc/health


Быстрый тест аутентификации
1) Создайте пользователя (POST /api/v1/auth/user/) с телом вида:
   {
     "name": "admin",
     "email": "admin@admin.ru",
     "password": "admin"
   }

2) Получите токен:
   curl -X POST \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "grant_type=password&username=admin@admin.ru&password=admin" \
     http://localhost:8000/api/v1/auth/token

3) Используйте Bearer-токен для защищенных эндпоинтов, например:
   GET /api/v1/auth/user/me


Переменные окружения и конфигурация (Dynaconf)
Базовые значения заданы в settings.toml. Любую настройку можно переопределить переменными окружения по схеме DYNACONF_SECTION__KEY (UPPER_CASE). Основные поля:

- [app_settings]
  - app_host (str, по умолчанию 0.0.0.0)
  - app_port (int, по умолчанию 8000)
  - app_use_testcontainers (bool) — при true интеграционные тесты поднимут PostgreSQL через testcontainers

- [db_settings]
  - db_name (str, по умолчанию test_db)
  - db_user (str, по умолчанию user)
  - db_password (str, по умолчанию password)
  - db_host (str, по умолчанию localhost)
  - db_port (int, по умолчанию 5432)

- [jwt_settings]
  - jwt_secret (str)
  - jwt_algorithm (str, по умолчанию HS256)
  - jwt_access_token_expire_minutes (int, по умолчанию 30)
  - jwt_bypass_auth (bool, по умолчанию false)

Примеры переопределения через переменные окружения:
  export DYNACONF_APP_SETTINGS__APP_PORT=8080
  export DYNACONF_DB_SETTINGS__DB_HOST=127.0.0.1
  export DYNACONF_JWT_SETTINGS__JWT_SECRET="your-very-secret"


Работа с БД и миграциями
- Создать новую миграцию (опциональная метка ветки через BRANCH):
  make mkmigrate BRANCH=my_feature

- Применить миграции:
  make migrate


Скрипты (Makefile)
- format — автоформатирование кода (ruff)
- type — проверка типов (mypy)
- dev — запуск dev-сервера (fastapi dev)
- run — запуск prod-сервера (fastapi run)
- ddev — поднять тестовый postgres из docker-compose (docker/docker-compose.test.yml)
- mkmigrate — сгенерировать миграции Alembic
- migrate — применить миграции Alembic
- utest — запустить юнит-тесты
- itest — запустить интеграционные тесты


Тесты
- Юнит-тесты:
  make utest

- Интеграционные тесты (две опции):
  1) С testcontainers (по умолчанию, если app_use_testcontainers=true в settings.toml):
     make itest
  2) С внешним PostgreSQL:
     - Поднимите БД:
       make ddev
     - Убедитесь, что настройки БД в settings.toml указывают на поднятый postgres
     - Запустите:
       make itest


Запуск в Docker
1) Сборка образа:
   docker build -t personal-assistant:latest .

2) Запуск:
   docker run --rm -p 8000:8000 \
     -e DB_SETTINGS__DB_HOST=host.docker.internal \
     -e DB_SETTINGS__DB_PORT=5432 \
     -e DB_SETTINGS__DB_USER=user \
     -e DB_SETTINGS__DB_PASSWORD=password \
     -e DB_SETTINGS__DB_NAME=test_db \
     personal-assistant:latest

Примечание: по умолчанию контейнер выполняет make run (fastapi run personal_assistant/src/main.py). Для работы пользовательских эндпоинтов необходим доступный PostgreSQL.


Структура проекта (основное)
personal_assistant/
  src/
    main.py                — точка входа приложения (FastAPI app)
    api/                   — роутеры и зависимости
    configs/               — типизированные конфиги (Dynaconf → Pydantic)
    models/                — модели БД и сессии
    repositories/          — доступ к данным
    services/              — бизнес-логика (аутентификация и т.п.)
    schemas/               — Pydantic-схемы
    alembic*/              — миграции Alembic
  tests/                   — юнит-тесты
  integrational_tests/     — интеграционные тесты


Лицензия
Проект распространяется по лицензии MIT — см. файл LICENSE.


CI/CD
GitHub Actions выполняет:
- Юнит-тесты и интеграционные тесты (с PostgreSQL)
- На ветке main при успехе — сборка и публикация Docker-образа в GHCR
