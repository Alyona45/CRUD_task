from fastapi import APIRouter, Depends, status

from app.schemas.user import TokenResponse, UserLogin, UserRead, UserRegister
from app.services.user_service import UserService


router = APIRouter(prefix="/v1/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserRegister, service: UserService = Depends()) -> UserRead:
    return service.register_user(user_data)


@router.post("/login", response_model=TokenResponse)
def login_user(credentials: UserLogin, service: UserService = Depends()) -> TokenResponse:
    return service.authenticate_user(credentials)
