from typing import List

from fastapi import APIRouter, Depends, File, Response, UploadFile, status

from app.core.auth import get_current_user
from app.models.user import User
from app.schemas.task import TaskAvatarResponse, TaskCreate, TaskResponse, TaskUpdate
from app.services.task_service import TaskService


router = APIRouter(prefix="/v1/tasks", tags=["tasks"])


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task_endpoint(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user),
    service: TaskService = Depends(),
) -> TaskResponse:
    return await service.create_task(current_user, task_data)


@router.get("", response_model=List[TaskResponse])
async def get_tasks_endpoint(
    current_user: User = Depends(get_current_user),
    service: TaskService = Depends(),
) -> List[TaskResponse]:
    return await service.get_tasks(current_user)


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task_endpoint(
    task_id: int,
    current_user: User = Depends(get_current_user),
    service: TaskService = Depends(),
) -> TaskResponse:
    return await service.get_task_by_id(current_user, task_id)


@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task_endpoint(
    task_id: int,
    task_data: TaskUpdate,
    current_user: User = Depends(get_current_user),
    service: TaskService = Depends(),
) -> TaskResponse:
    return await service.update_task(current_user, task_id, task_data)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task_endpoint(
    task_id: int,
    current_user: User = Depends(get_current_user),
    service: TaskService = Depends(),
) -> Response:
    await service.delete_task(current_user, task_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{task_id}/upload-avatar", response_model=TaskAvatarResponse)
async def upload_task_avatar_endpoint(
    task_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    service: TaskService = Depends(),
) -> TaskAvatarResponse:
    avatar_url = await service.upload_avatar(current_user, task_id, file)
    return TaskAvatarResponse(url=avatar_url)


@router.get("/{task_id}/avatar", response_model=TaskAvatarResponse)
async def get_task_avatar_endpoint(
    task_id: int,
    current_user: User = Depends(get_current_user),
    service: TaskService = Depends(),
) -> TaskAvatarResponse:
    avatar_url = await service.get_avatar_url(current_user, task_id)
    return TaskAvatarResponse(url=avatar_url)
