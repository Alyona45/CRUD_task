from unittest.mock import AsyncMock

import pytest
from fastapi import status
from sqlalchemy.exc import SQLAlchemyError

from app.api.system import healthcheck, info


@pytest.mark.asyncio
async def test_info_returns_version_and_environment():
    response = await info()

    assert response == {
        "version": "0.1.0",
        "environment": "dev",
    }


@pytest.mark.asyncio
async def test_healthcheck_returns_ok_when_dependencies_are_healthy(monkeypatch):
    db = AsyncMock()
    monkeypatch.setattr("app.api.system.check_storage_health", AsyncMock(return_value=True))

    response = await healthcheck(db=db)

    db.execute.assert_awaited_once()
    assert response == {
        "status": "ok",
        "database": "ok",
        "storage": "ok",
    }


@pytest.mark.asyncio
async def test_healthcheck_returns_503_payload_when_database_or_storage_is_down(monkeypatch):
    db = AsyncMock()
    db.execute.side_effect = SQLAlchemyError("db down")
    monkeypatch.setattr("app.api.system.check_storage_health", AsyncMock(return_value=False))

    response = await healthcheck(db=db)

    assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
    assert response.body == b'{"status":"error","database":"error","storage":"error"}'
