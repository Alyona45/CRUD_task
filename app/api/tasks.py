from typing import List

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.models import get_db
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.services.task_service import (
    create_task,
    delete_task,
    get_task_by_id,
    get_tasks,
    update_task,
)


router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task_endpoint(task_data: TaskCreate, db: Session = Depends(get_db)) -> TaskResponse:
    return create_task(db, task_data)


@router.get("", response_model=List[TaskResponse])
def get_tasks_endpoint(db: Session = Depends(get_db)) -> List[TaskResponse]:
    return get_tasks(db)


@router.get("/{task_id}", response_model=TaskResponse)
def get_task_endpoint(task_id: int, db: Session = Depends(get_db)) -> TaskResponse:
    return get_task_by_id(db, task_id)


@router.patch("/{task_id}", response_model=TaskResponse)
def update_task_endpoint(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
) -> TaskResponse:
    return update_task(db, task_id, task_data)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task_endpoint(task_id: int, db: Session = Depends(get_db)) -> Response:
    delete_task(db, task_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
