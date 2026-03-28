from fastapi import Depends

from app.core.exceptions import TaskNotFound
from app.models.user import User
from app.repositories.comment_repository import CommentRepository
from app.repositories.task_repository import TaskRepository
from app.schemas.comment import CommentCreate


class CommentService:
    def __init__(
        self,
        comment_repository: CommentRepository = Depends(),
        task_repository: TaskRepository = Depends(),
    ):
        self.comment_repository = comment_repository
        self.task_repository = task_repository

    def create_comment(self, current_user: User, task_id: int, comment_data: CommentCreate):
        task = self.task_repository.get_by_id_for_owner(task_id, current_user.id)
        if task is None:
            raise TaskNotFound()
        return self.comment_repository.create(task.id, comment_data)

    def get_comments(self, current_user: User, task_id: int):
        task = self.task_repository.get_by_id_for_owner(task_id, current_user.id)
        if task is None:
            raise TaskNotFound()
        return self.comment_repository.get_all_by_task(task.id)
