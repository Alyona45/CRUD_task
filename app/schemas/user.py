from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator


class UserBase(BaseModel):
    name: str = Field(min_length=2)
    surname: str = Field(min_length=2)
    email: EmailStr

    @field_validator("name")
    @classmethod
    def validate_name_letters_only(cls, value: str) -> str:
        if not value.isalpha():
            raise ValueError("name must contain only alphabetic characters")
        return value


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2)
    surname: Optional[str] = Field(default=None, min_length=2)
    email: Optional[EmailStr] = None

    @field_validator("name")
    @classmethod
    def validate_name_letters_only(cls, value: Optional[str]) -> Optional[str]:
        if value is not None and not value.isalpha():
            raise ValueError("name must contain only alphabetic characters")
        return value


class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True
