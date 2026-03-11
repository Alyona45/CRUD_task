from typing import Optional

from pydantic import BaseModel, Field, field_validator


class TaskBase(BaseModel):
    title: str = Field(min_length=3, max_length=255)
    description: Optional[str] = None
    is_done: bool = False

    @field_validator("title")
    @classmethod
    def validate_title_not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("title must not be blank")
        return value


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=3, max_length=255)
    description: Optional[str] = None
    is_done: Optional[bool] = None

    @field_validator("title")
    @classmethod
    def validate_title_not_blank(cls, value: Optional[str]) -> Optional[str]:
        if value is not None and not value.strip():
            raise ValueError("title must not be blank")
        return value


class TaskResponse(TaskBase):
    id: int

    class Config:
        from_attributes = True
