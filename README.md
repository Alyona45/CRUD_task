# CRUD Task

Minimal FastAPI backend with CRUD operations for tasks.

## Stack

- FastAPI
- SQLAlchemy
- Pydantic
- Alembic
- PostgreSQL

## Run

```bash
./venv/bin/pip install -e .
cp .env.example .env
./venv/bin/alembic upgrade head
./venv/bin/uvicorn app.main:app --reload
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

- `POST /auth/register`
- `POST /auth/login`
- `POST /tasks`
- `GET /tasks`
- `GET /tasks/{task_id}`
- `PATCH /tasks/{task_id}`
- `DELETE /tasks/{task_id}`
