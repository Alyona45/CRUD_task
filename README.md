# CRUD Task

Minimal FastAPI backend with async CRUD operations for tasks and comments, file uploads to MinIO, health checks, and Docker-based local launch.

## Stack

- FastAPI
- SQLAlchemy Async
- Pydantic
- Alembic
- PostgreSQL
- MinIO
- Pytest

## Run Locally

```bash
./venv/bin/pip install -e .[dev]
cp .env.example .env
./venv/bin/alembic upgrade head
./venv/bin/uvicorn app.main:app --reload
```

## Run With Docker

```bash
sudo docker compose up --build
```

Services:

- API: `http://localhost:8000`
- MinIO API: `http://localhost:9000`
- MinIO Console: `http://localhost:9001`

## Tests

```bash
./venv/bin/pytest
```

## Environment

Set your application configuration in `.env`:

```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/crud_task
SECRET_KEY=replace-with-a-long-random-secret
ACCESS_TOKEN_EXPIRE_MINUTES=30
APP_ENV=dev
APP_VERSION=0.1.0
MINIO_ENDPOINT=http://localhost:9000
MINIO_PUBLIC_URL=http://localhost:9000
MINIO_ACCESS_KEY=your_minio_access_key
MINIO_SECRET_KEY=your_minio_secret_key
MINIO_BUCKET=your_bucket_name
MINIO_REGION=us-east-1
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
- `GET /info`
- `GET /health`
- `POST /v1/tasks`
- `GET /v1/tasks`
- `GET /v1/tasks/{task_id}`
- `PATCH /v1/tasks/{task_id}`
- `DELETE /v1/tasks/{task_id}`
- `POST /v1/tasks/{task_id}/upload-avatar`
- `GET /v1/tasks/{task_id}/avatar`
- `POST /v1/tasks/{task_id}/comments`
- `GET /v1/tasks/{task_id}/comments`
