from typing import List

from fastapi import APIRouter, Depends, Response, status

from app.core.auth import get_current_user
from app.models.user import User
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.services.task_service import TaskService


router = APIRouter(prefix="/v1/tasks", tags=["tasks"])


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task_endpoint(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user),
    service: TaskService = Depends(),
) -> TaskResponse:
    return service.create_task(current_user, task_data)


@router.get("", response_model=List[TaskResponse])
def get_tasks_endpoint(
    current_user: User = Depends(get_current_user),
    service: TaskService = Depends(),
) -> List[TaskResponse]:
    return service.get_tasks(current_user)


@router.get("/{task_id}", response_model=TaskResponse)
def get_task_endpoint(
    task_id: int,
    current_user: User = Depends(get_current_user),
    service: TaskService = Depends(),
) -> TaskResponse:
    return service.get_task_by_id(current_user, task_id)


@router.patch("/{task_id}", response_model=TaskResponse)
def update_task_endpoint(
    task_id: int,
    task_data: TaskUpdate,
    current_user: User = Depends(get_current_user),
    service: TaskService = Depends(),
) -> TaskResponse:
    return service.update_task(current_user, task_id, task_data)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task_endpoint(
    task_id: int,
    current_user: User = Depends(get_current_user),
    service: TaskService = Depends(),
) -> Response:
    service.delete_task(current_user, task_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
