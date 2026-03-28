import json
from types import SimpleNamespace

from app.core.exceptions import TaskNotFound
from app.main import app_error_handler


def test_task_not_found_handler_returns_expected_json():
    response = app_error_handler(SimpleNamespace(), TaskNotFound())

    assert response.status_code == 404
    assert json.loads(response.body) == {
        "error": {
            "code": "TASK_NOT_FOUND",
            "message": "Task not found",
        }
    }
