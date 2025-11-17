FROM python:3.12-slim

RUN apt update && apt install make

WORKDIR /app
COPY pyproject.toml poetry.lock ./

RUN pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi  --no-root --only main

COPY . .

CMD ["make", "run"]
