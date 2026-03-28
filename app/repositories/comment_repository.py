from fastapi import Depends
from sqlalchemy.orm import Session

from app.models import get_db
from app.models.comment import Comment
from app.schemas.comment import CommentCreate


class CommentRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def create(self, task_id: int, comment_data: CommentCreate) -> Comment:
        comment = Comment(task_id=task_id, **comment_data.model_dump())
        self.db.add(comment)
        self.db.commit()
        self.db.refresh(comment)
        return comment

    def get_all_by_task(self, task_id: int) -> list[Comment]:
        return self.db.query(Comment).filter(Comment.task_id == task_id).all()

    def get_by_id_for_task(self, comment_id: int, task_id: int) -> Comment | None:
        return (
            self.db.query(Comment)
            .filter(Comment.id == comment_id, Comment.task_id == task_id)
            .first()
        )
