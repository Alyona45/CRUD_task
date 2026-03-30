import os
from pathlib import Path
from urllib.parse import urlparse

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@localhost:5432/crud_task",
)

SECRET_KEY = os.getenv("SECRET_KEY", "change-me-for-production")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
APP_ENV = os.getenv("APP_ENV", "dev")
APP_VERSION = os.getenv("APP_VERSION", "0.1.0")
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "http://localhost:9000")
MINIO_PUBLIC_URL = os.getenv("MINIO_PUBLIC_URL", MINIO_ENDPOINT)
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minioadmin")
MINIO_BUCKET = os.getenv("MINIO_BUCKET", "task-files")
MINIO_REGION = os.getenv("MINIO_REGION", "us-east-1")

_parsed_minio_endpoint = urlparse(MINIO_ENDPOINT)
MINIO_HEALTH_HOST = _parsed_minio_endpoint.hostname or "localhost"
MINIO_HEALTH_PORT = _parsed_minio_endpoint.port or (
    443 if _parsed_minio_endpoint.scheme == "https" else 9000
)
MINIO_HEALTH_PATH = "/minio/health/live"
MINIO_HEALTH_SSL = _parsed_minio_endpoint.scheme == "https"
