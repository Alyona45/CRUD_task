from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.auth import router as auth_router
from app.api.comments import router as comments_router
from app.api.tasks import router as tasks_router
from app.core.exceptions import AppError


app = FastAPI(title="Task Manager API")


@app.exception_handler(AppError)
def app_error_handler(_: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
            }
        },
    )


app.include_router(auth_router)
app.include_router(tasks_router)
app.include_router(comments_router)
