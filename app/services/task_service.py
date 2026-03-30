import uuid

from fastapi import Depends
from fastapi import HTTPException, UploadFile, status

from app.core.exceptions import TaskAvatarNotFound, TaskNotFound
from app.core.storage import upload_file_to_storage
from app.models.user import User
from app.repositories.task_repository import TaskRepository
from app.schemas.task import TaskCreate, TaskUpdate


class TaskService:
    def __init__(self, task_repository: TaskRepository = Depends()):
        self.task_repository = task_repository

    async def create_task(self, current_user: User, task_data: TaskCreate):
        return await self.task_repository.create(current_user.id, task_data)

    async def get_tasks(self, current_user: User):
        return await self.task_repository.get_all_by_owner(current_user.id)

    async def get_task_by_id(self, current_user: User, task_id: int):
        task = await self.task_repository.get_by_id_for_owner(task_id, current_user.id)
        if task is None:
            raise TaskNotFound()
        return task

    async def update_task(self, current_user: User, task_id: int, task_data: TaskUpdate):
        task = await self.get_task_by_id(current_user, task_id)
        return await self.task_repository.update(task, task_data)

    async def delete_task(self, current_user: User, task_id: int) -> None:
        task = await self.get_task_by_id(current_user, task_id)
        await self.task_repository.delete(task)

    async def upload_avatar(self, current_user: User, task_id: int, file: UploadFile) -> str:
        task = await self.get_task_by_id(current_user, task_id)

        if not file.filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Filename is required",
            )

        extension = file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
        if extension not in {"jpg", "jpeg", "png"}:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid avatar format",
            )

        content = await file.read()
        key = f"tasks/{task.id}/avatars/{uuid.uuid4()}.{extension}"
        avatar_url = await upload_file_to_storage(
            content=content,
            key=key,
            content_type=file.content_type or "application/octet-stream",
        )
        await self.task_repository.set_avatar_url(task, avatar_url)
        return avatar_url

    async def get_avatar_url(self, current_user: User, task_id: int) -> str:
        task = await self.get_task_by_id(current_user, task_id)
        if task.avatar_url is None:
            raise TaskAvatarNotFound()
        return task.avatar_url
