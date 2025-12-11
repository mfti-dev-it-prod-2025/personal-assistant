# Personal Assistant

![Python 3.12](https://img.shields.io/badge/python-3.12-blue)
![FastAPI](https://img.shields.io/badge/fastapi-latest-brightgreen)
![PostgreSQL](https://img.shields.io/badge/postgresql-16+-blueviolet)
![License](https://img.shields.io/badge/license-MIT-yellow)

Personal Assistant — веб‑сервис для управления личными финансами, заметками, задачами и событиями через единое API.

## Ключевые возможности

- **Бюджетирование**: учёт транзакций (доходы/расходы).
- **Задачи**: создание, редактирование, удаление и просмотр.
- **Заметки**: создание, редактирование, удаление и просмотр.
- **События**: создание, редактирование, удаление, просмотр и напоминания.
- **Безопасность**:
  - регистрация и аутентификация (JWT);
  - ролевая модель доступа.
- **API**:
  - REST API с документацией (Swagger UI / Redoc);
  - поддержка JSON‑формата;
  - версионирование;
  - готовые Pydantic‑схемы.

## Технический стек

- **Язык и фреймворк**: Python 3.12, FastAPI.
- **БД и ORM**: PostgreSQL 16+, SQLModel (SQLAlchemy), asyncpg.
- **Миграции**: Alembic.
- **Конфигурация**: Dynaconf + Pydantic‑модели.
- **Сервер**: uvicorn (fastapi CLI).
- **Тестирование**:
  - юнит‑тесты: `pytest`, `pytest-asyncio`;
  - интеграционные: `testcontainers` (PostgreSQL).
- **Качество кода**: `ruff` (форматирование), `mypy` (типизация).
- **Пакетный менеджер**: Poetry 2.x.
- **Контейнеризация**: Docker.
- **CI/CD**: GitHub Actions, GNU Make.

## Начало работы

### Установка

Клонировать репозиторий:

```bash
git clone git@github.com:mfti-dev-it-prod-2025/personal-assistant.git
cd personal-assistant
```

Установить зависимости:

```bash
pip install -U poetry
poetry install
```

Настройте БД:

- Запустите PostgreSQL (локально или через Docker) (см. ниже).
- Примените миграции:

```bash
make migrate
```

### Запуск

- Режим разработки (с автоперезагрузкой):

```bash
make dev
```

- Прод-режим:

```bash
make run
```

- Альтернатива через uvicorn:

```bash
poetry run uvicorn personal_assistant.src.main:app --host 0.0.0.0 --port 8000
```

После запуска доступны:

- Swagger UI: `http://localhost:8000/docs`
- Redoc: `http://localhost:8000/redoc`
- Health‑check: `http://localhost:8000/api/v1/misc/health`

### Аутентификация (быстрый старт)

Создайте пользователя:

```bash
curl -X POST http://localhost:8000/api/v1/auth/user/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "admin",
    "email": "admin@admin.ru",
    "password": "admin"
  }'
```

Получите JWT‑токен:

```bash
curl -X POST \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=password&username=admin@admin.ru&password=admin" \
  http://localhost:8000/api/v1/auth/token
```

Используйте токен для доступа к защищённым эндпоинтам:

```bash
curl -X GET http://localhost:8000/api/v1/auth/user/me \
  -H "Authorization: Bearer <your-token>"
```

### Конфигурация

Основные настройки задаются в settings.toml. Переопределить их можно через переменные окружения по схеме DYNACONF_SECTION__KEY (в верхнем регистре).

#### Основные секции

- `[app_settings]`
  - `app_host` (str, по умолчанию `0.0.0.0`)
  - `app_port` (int, по умолчанию `8000`)
  - `app_use_testcontainers` (bool) — при `true` интеграционные тесты поднимут PostgreSQL через testcontainers
- `[db_settings]`
  - `db_name` (str, по умолчанию `test_db`)
  - `db_user` (str, по умолчанию `user`)
  - `db_password` (str, по умолчанию `password`)
  - `db_host` (str, по умолчанию `localhost`)
  - `db_port` (int, по умолчанию `5432`)
- `[jwt_settings]`
  - `jwt_secret` (str)
  - `jwt_algorithm` (str, по умолчанию `HS256`)
  - `jwt_access_token_expire_minutes` (int, по умолчанию `30`)
  - `jwt_bypass_auth` (bool, по умолчанию `false`)

Примеры переопределения через переменные окружения:

```bash
export DYNACONF_APP_SETTINGS__APP_PORT=8080
export DYNACONF_DB_SETTINGS__DB_HOST=127.0.0.1
export DYNACONF_JWT_SETTINGS__JWT_SECRET="your-very-secret"
```

### Работа с БД и миграциями

- Создать новую миграцию (с меткой ветки):

```bash
  make mkmigrate BRANCH=my_feature
```

- Применить миграции:

```bash
make migrate
```

### Тестирование

#### Юнит-тесты

```bash
make utest
```

#### Интеграционные тесты (два варианта)

Через testcontainers (по умолчанию, если `app_use_testcontainers=true` в `settings.toml)`:

```bash
make itest
```

Через внешний PostgreSQL:

- Поднимите БД:

```bash
make ddev
```

- Убедитесь, что настройки БД в settings.toml указывают на поднятый PostgreSQL.
- Запустите тесты:

```bash
make itest
```

### Запуск в Docker

Соберите образ:

```bash
docker build -t personal-assistant:latest .
```

Запустите контейнер:

```bash
docker run --rm -p 8000:8000 \
  -e DB_SETTINGS__DB_HOST=host.docker.internal \
  -e DB_SETTINGS__DB_PORT=5432 \
  -e DB_SETTINGS__DB_USER=user \
  -e DB_SETTINGS__DB_PASSWORD=password \
  -e DB_SETTINGS__DB_NAME=test_db \
  personal-assistant:latest
```

> Примечание: по умолчанию контейнер выполняет `make run`. Для работы требуется доступный PostgreSQL.

## Структура проекта (основное)

```bash
personal_assistant/
├── src/                  # Основной код
│   ├── main.py           # Точка входа (FastAPI app)
│   ├── api/              # Роутеры и зависимости
│   ├── configs/          # Конфигурации (Dynaconf → Pydantic)
│   ├── models/           # Модели БД и сессии
│   ├── repositories/     # Доступ к данным
│   ├── services/         # Бизнес‑логика
│   ├── schemas/          # Pydantic‑схемы
│   └── alembic/          # Миграции
├── tests/                # Юнит‑тесты
├── integrational_tests/  # Интеграционные тесты
├── settings.toml         # Основные настройки
├── Makefile              # Скрипты разработки
├── Dockerfile            # Сборка контейнера
```

### Точки входа и ключевые файлы

- Приложение:
  - `personal_assistant/src/main.py` (объект FastAPI: `app`).
  - Uvicorn‑путь: `personal_assistant.src.main:app`.
- Настройки:
  - Основной файл: settings.toml (в корне репозитория).
  - Переопределение: переменные окружения (`DYNACONF_...`).
- Скрипты
  - `Makefile` — основные сценарии разработки, запуска и тестов.
  - `Dockerfile` — сборка Docker‑образа.

## Доступные команды Makefile

- `format` — автоформатирование кода (`ruff`)
- `type` — проверка типов (`mypy`)
- `dev` — запуск dev-сервера (`fastapi dev`)
- `run` — запуск prod-сервера (`fastapi run`)
- `ddev` — поднять тестовый postgres из `docker-compose` (`docker/docker-compose.test.yml`)
- `mkmigrate` — сгенерировать новую миграцию Alembic (с опциональной меткой ветки через `BRANCH=`).
- `migrate` — применить миграции Alembic
- `utest` — запустить юнит-тесты
- `itest` — запустить интеграционные тесты

## CI/CD

GitHub Actions автоматически выполняет:

- Юнит‑тесты и интеграционные тесты (с PostgreSQL).
- На ветке `main` при успешном прохождении тестов:
  - сборку Docker‑образа;
  - публикацию в GitHub Container Registry (GHCR).

## Лицензия

Проект распространяется под лицензией [MIT](LICENSE).
