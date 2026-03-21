from fastapi import Depends, HTTPException, status
from app.models.user import User
from app.repositories.task_repository import TaskRepository
from app.schemas.task import TaskCreate, TaskUpdate


class TaskService:
    def __init__(self, task_repository: TaskRepository = Depends()):
        self.task_repository = task_repository

    def create_task(self, current_user: User, task_data: TaskCreate):
        return self.task_repository.create(current_user.id, task_data)

    def get_tasks(self, current_user: User):
        return self.task_repository.get_all_by_owner(current_user.id)

    def get_task_by_id(self, current_user: User, task_id: int):
        task = self.task_repository.get_by_id_for_owner(task_id, current_user.id)
        if task is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )
        return task

    def update_task(self, current_user: User, task_id: int, task_data: TaskUpdate):
        task = self.get_task_by_id(current_user, task_id)
        return self.task_repository.update(task, task_data)

    def delete_task(self, current_user: User, task_id: int) -> None:
        task = self.get_task_by_id(current_user, task_id)
        self.task_repository.delete(task)
