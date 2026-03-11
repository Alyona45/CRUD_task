from typing import List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


def create_task(db: Session, task_data: TaskCreate) -> Task:
    task = Task(**task_data.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def get_tasks(db: Session) -> List[Task]:
    return db.query(Task).all()


def get_task_by_id(db: Session, task_id: int) -> Task:
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    return task


def update_task(db: Session, task_id: int, task_data: TaskUpdate) -> Task:
    task = get_task_by_id(db, task_id)

    for field, value in task_data.model_dump(exclude_unset=True).items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task_id: int) -> None:
    task = get_task_by_id(db, task_id)
    db.delete(task)
    db.commit()
