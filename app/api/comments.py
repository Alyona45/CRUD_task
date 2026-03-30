from typing import List

from fastapi import APIRouter, Depends, status

from app.core.auth import get_current_user
from app.models.user import User
from app.schemas.comment import CommentCreate, CommentResponse
from app.services.comment_service import CommentService


router = APIRouter(prefix="/v1/tasks/{task_id}/comments", tags=["comments"])


@router.post("", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def create_comment_endpoint(
    task_id: int,
    comment_data: CommentCreate,
    current_user: User = Depends(get_current_user),
    service: CommentService = Depends(),
) -> CommentResponse:
    return await service.create_comment(current_user, task_id, comment_data)


@router.get("", response_model=List[CommentResponse])
async def get_comments_endpoint(
    task_id: int,
    current_user: User = Depends(get_current_user),
    service: CommentService = Depends(),
) -> List[CommentResponse]:
    return await service.get_comments(current_user, task_id)
