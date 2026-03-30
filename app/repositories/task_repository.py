from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import get_db
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


class TaskRepository:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def create(self, owner_id: int, task_data: TaskCreate) -> Task:
        task = Task(owner_id=owner_id, **task_data.model_dump())
        self.db.add(task)
        await self.db.commit()
        await self.db.refresh(task)
        return task

    async def get_all_by_owner(self, owner_id: int) -> list[Task]:
        result = await self.db.execute(select(Task).where(Task.owner_id == owner_id))
        return result.scalars().all()

    async def get_by_id_for_owner(self, task_id: int, owner_id: int) -> Task | None:
        result = await self.db.execute(
            select(Task).where(Task.id == task_id, Task.owner_id == owner_id)
        )
        return result.scalar_one_or_none()

    async def update(self, task: Task, task_data: TaskUpdate) -> Task:
        for field, value in task_data.model_dump(exclude_unset=True).items():
            setattr(task, field, value)

        await self.db.commit()
        await self.db.refresh(task)
        return task

    async def set_avatar_url(self, task: Task, avatar_url: str) -> Task:
        task.avatar_url = avatar_url
        await self.db.commit()
        await self.db.refresh(task)
        return task

    async def delete(self, task: Task) -> None:
        await self.db.delete(task)
        await self.db.commit()
