from fastapi import APIRouter, Depends, Response, status
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.storage import check_storage_health
from app.models import get_db
from app.settings import APP_ENV, APP_VERSION


router = APIRouter(tags=["system"])


@router.get("/health")
async def healthcheck(db: AsyncSession = Depends(get_db)) -> Response:
    database_status = "ok"
    storage_status = "ok"

    try:
        await db.execute(text("SELECT 1"))
    except Exception:
        database_status = "error"

    if not await check_storage_health():
        storage_status = "error"

    if database_status == "error" or storage_status == "error":
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "error",
                "database": database_status,
                "storage": storage_status,
            },
        )

    return {
        "status": "ok",
        "database": database_status,
        "storage": storage_status,
    }


@router.get("/info")
async def info() -> dict[str, str]:
    return {
        "version": APP_VERSION,
        "environment": APP_ENV,
    }
