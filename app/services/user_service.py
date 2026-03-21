from fastapi import Depends, HTTPException, status

from app.core.security import create_access_token, hash_password, verify_password
from app.repositories.user_repository import UserRepository
from app.schemas.user import TokenResponse, UserLogin, UserRegister


class UserService:
    def __init__(self, user_repository: UserRepository = Depends()):
        self.user_repository = user_repository

    def register_user(self, user_data: UserRegister):
        if self.user_repository.get_by_email(user_data.email) is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists",
            )

        if self.user_repository.get_by_username(user_data.username) is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this username already exists",
            )

        return self.user_repository.create(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hash_password(user_data.password),
        )

    def authenticate_user(self, credentials: UserLogin) -> TokenResponse:
        user = self.user_repository.get_by_username(credentials.username)
        if user is None or not verify_password(credentials.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
            )

        return TokenResponse(
            access_token=create_access_token({"sub": user.username}),
            token_type="bearer",
        )
