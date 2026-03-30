from io import BytesIO
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest
from starlette.datastructures import UploadFile

from app.core.exceptions import TaskAvatarNotFound
from app.services.task_service import TaskService


@pytest.mark.asyncio
async def test_upload_avatar_saves_generated_url(monkeypatch):
    task = SimpleNamespace(id=7, avatar_url=None)
    task_repository = AsyncMock()
    task_repository.get_by_id_for_owner.return_value = task
    task_repository.set_avatar_url.return_value = task

    async def fake_upload_file_to_storage(content: bytes, key: str, content_type: str) -> str:
        assert content == b"avatar-bytes"
        assert key.startswith("tasks/7/avatars/")
        assert content_type == "image/png"
        return "http://localhost:9000/task-files/tasks/7/avatars/generated.png"

    monkeypatch.setattr(
        "app.services.task_service.upload_file_to_storage",
        fake_upload_file_to_storage,
    )

    service = TaskService(task_repository=task_repository)
    current_user = SimpleNamespace(id=42)
    upload = UploadFile(filename="avatar.png", file=BytesIO(b"avatar-bytes"))
    upload.headers = {"content-type": "image/png"}

    avatar_url = await service.upload_avatar(current_user, task.id, upload)

    assert avatar_url == "http://localhost:9000/task-files/tasks/7/avatars/generated.png"
    task_repository.set_avatar_url.assert_awaited_once_with(task, avatar_url)


@pytest.mark.asyncio
async def test_get_avatar_url_raises_when_avatar_missing():
    task = SimpleNamespace(id=7, avatar_url=None)
    task_repository = AsyncMock()
    task_repository.get_by_id_for_owner.return_value = task

    service = TaskService(task_repository=task_repository)
    current_user = SimpleNamespace(id=42)

    with pytest.raises(TaskAvatarNotFound):
        await service.get_avatar_url(current_user, task.id)
