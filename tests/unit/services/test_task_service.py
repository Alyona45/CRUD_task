from types import SimpleNamespace
from unittest.mock import Mock

from app.schemas.task import TaskCreate
from app.services.task_service import TaskService


def test_create_task_uses_repository_with_current_user_id():
    task_repository = Mock()
    expected_task = SimpleNamespace(id=1, title="Test task")
    task_repository.create.return_value = expected_task

    service = TaskService(task_repository=task_repository)
    current_user = SimpleNamespace(id=42)
    task_data = TaskCreate(title="Test task", description="Desc", is_done=False)

    result = service.create_task(current_user, task_data)

    task_repository.create.assert_called_once_with(42, task_data)
    assert result is expected_task
