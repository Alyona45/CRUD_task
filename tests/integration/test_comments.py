from collections.abc import Callable

from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.comment_repository import CommentRepository
from app.repositories.task_repository import TaskRepository
from app.schemas.comment import CommentCreate
from app.schemas.task import TaskCreate
from app.services.comment_service import CommentService
from app.services.task_service import TaskService


def test_create_and_get_comments_for_task(db_session_factory: Callable[[], Session]):
    with db_session_factory() as db_session:
        user = User(
            username="comment_owner",
            email="comment_owner@example.com",
            hashed_password="not-used-in-this-test",
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        task_service = TaskService(task_repository=TaskRepository(db=db_session))
        comment_service = CommentService(
            comment_repository=CommentRepository(db=db_session),
            task_repository=TaskRepository(db=db_session),
        )

        task = task_service.create_task(
            user,
            TaskCreate(
                title="Task with comments",
                description="Need comments",
                is_done=False,
            ),
        )

        created_comment = comment_service.create_comment(
            user,
            task.id,
            CommentCreate(content="First comment"),
        )
        comments = comment_service.get_comments(user, task.id)

        assert created_comment.id == 1
        assert created_comment.content == "First comment"
        assert created_comment.task_id == task.id
        assert len(comments) == 1
        assert comments[0].content == "First comment"
        assert comments[0].task_id == task.id
