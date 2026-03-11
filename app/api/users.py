from typing import List

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.models import get_db
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.services.user_service import (
    create_user,
    delete_user,
    get_user_by_id,
    get_users,
    update_user,
)


router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user_endpoint(user_data: UserCreate, db: Session = Depends(get_db)) -> UserResponse:
    return create_user(db, user_data)


@router.get("", response_model=List[UserResponse])
def get_users_endpoint(db: Session = Depends(get_db)) -> List[UserResponse]:
    return get_users(db)


@router.get("/{user_id}", response_model=UserResponse)
def get_user_endpoint(user_id: int, db: Session = Depends(get_db)) -> UserResponse:
    return get_user_by_id(db, user_id)


@router.patch("/{user_id}", response_model=UserResponse)
def update_user_endpoint(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
) -> UserResponse:
    return update_user(db, user_id, user_data)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_endpoint(user_id: int, db: Session = Depends(get_db)) -> Response:
    delete_user(db, user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
