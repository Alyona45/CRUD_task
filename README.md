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
pip install -r requirements.txt
cp .env.example .env
alembic upgrade head
uvicorn app.main:app --reload
```

## Environment

Set your PostgreSQL connection in `.env`:

```env
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/crud_task
```

## Alembic

Create a migration:

```bash
alembic revision --autogenerate -m "create users table"
```

Apply migrations:

```bash
alembic upgrade head
```

## Endpoints

- `POST /tasks`
- `GET /tasks`
- `GET /tasks/{task_id}`
- `PATCH /tasks/{task_id}`
- `DELETE /tasks/{task_id}`
