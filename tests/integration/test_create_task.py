from collections.abc import Callable

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task
from app.models.user import User
from app.repositories.task_repository import TaskRepository
from app.schemas.task import TaskCreate
from app.services.task_service import TaskService


@pytest.mark.asyncio
@pytest.mark.usefixtures("reset_database")
async def test_create_task_persists_task_in_database(
    db_session_factory: Callable[[], AsyncSession],
):
    async with db_session_factory() as db_session:
        user = User(
            username="task_owner",
            email="task_owner@example.com",
            hashed_password="not-used-in-this-test",
        )
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)

        service = TaskService(task_repository=TaskRepository(db=db_session))
        task_data = TaskCreate(
            title="Write integration test",
            description="Cover task creation flow",
            is_done=False,
        )

        created_task = await service.create_task(user, task_data)

        assert created_task.id == 1
        assert created_task.title == "Write integration test"
        assert created_task.description == "Cover task creation flow"
        assert created_task.is_done is False
        assert created_task.owner_id == user.id

    async with db_session_factory() as db_session:
        result = await db_session.execute(select(Task).where(Task.id == 1))
        stored_task = result.scalar_one()
        assert stored_task.title == "Write integration test"
        assert stored_task.description == "Cover task creation flow"
        assert stored_task.is_done is False
        assert stored_task.owner_id == 1
