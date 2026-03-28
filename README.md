# CRUD Task

Minimal FastAPI backend with CRUD operations for tasks and comments.

## Stack

- FastAPI
- SQLAlchemy
- Pydantic
- Alembic
- PostgreSQL
- Pytest

## Run

```bash
./venv/bin/pip install -e .
cp .env.example .env
./venv/bin/alembic upgrade head
./venv/bin/uvicorn app.main:app --reload
```

## Tests

```bash
./venv/bin/pip install -e .[dev]
./venv/bin/pytest
```

## Environment

Set your PostgreSQL connection in `.env`:

```env
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/crud_task
SECRET_KEY=replace-with-a-long-random-secret
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Alembic

Create a migration:

```bash
./venv/bin/alembic revision --autogenerate -m "create tasks table"
```

Apply migrations:

```bash
./venv/bin/alembic upgrade head
```

## Endpoints

- `POST /v1/auth/register`
- `POST /v1/auth/login`
- `POST /v1/tasks`
- `GET /v1/tasks`
- `GET /v1/tasks/{task_id}`
- `PATCH /v1/tasks/{task_id}`
- `DELETE /v1/tasks/{task_id}`
- `POST /v1/tasks/{task_id}/comments`
- `GET /v1/tasks/{task_id}/comments`
