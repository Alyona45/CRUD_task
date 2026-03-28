from fastapi import status


class AppError(Exception):
    status_code = status.HTTP_400_BAD_REQUEST
    code = "APP_ERROR"
    message = "Application error"

    def __init__(self, message: str | None = None):
        if message is not None:
            self.message = message
        super().__init__(self.message)


class TaskNotFound(AppError):
    status_code = status.HTTP_404_NOT_FOUND
    code = "TASK_NOT_FOUND"
    message = "Task not found"


class CommentNotFound(AppError):
    status_code = status.HTTP_404_NOT_FOUND
    code = "COMMENT_NOT_FOUND"
    message = "Comment not found"
