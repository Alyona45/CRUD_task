from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import get_db
from app.models.comment import Comment
from app.schemas.comment import CommentCreate


class CommentRepository:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def create(self, task_id: int, comment_data: CommentCreate) -> Comment:
        comment = Comment(task_id=task_id, **comment_data.model_dump())
        self.db.add(comment)
        await self.db.commit()
        await self.db.refresh(comment)
        return comment

    async def get_all_by_task(self, task_id: int) -> list[Comment]:
        result = await self.db.execute(select(Comment).where(Comment.task_id == task_id))
        return result.scalars().all()

    async def get_by_id_for_task(self, comment_id: int, task_id: int) -> Comment | None:
        result = await self.db.execute(
            select(Comment).where(Comment.id == comment_id, Comment.task_id == task_id)
        )
        return result.scalar_one_or_none()
