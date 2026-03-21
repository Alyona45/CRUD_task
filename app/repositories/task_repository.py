from fastapi import Depends
from sqlalchemy.orm import Session

from app.models import get_db
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


class TaskRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def create(self, owner_id: int, task_data: TaskCreate) -> Task:
        task = Task(owner_id=owner_id, **task_data.model_dump())
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def get_all_by_owner(self, owner_id: int) -> list[Task]:
        return self.db.query(Task).filter(Task.owner_id == owner_id).all()

    def get_by_id_for_owner(self, task_id: int, owner_id: int) -> Task | None:
        return self.db.query(Task).filter(Task.id == task_id, Task.owner_id == owner_id).first()

    def update(self, task: Task, task_data: TaskUpdate) -> Task:
        for field, value in task_data.model_dump(exclude_unset=True).items():
            setattr(task, field, value)

        self.db.commit()
        self.db.refresh(task)
        return task

    def delete(self, task: Task) -> None:
        self.db.delete(task)
        self.db.commit()
