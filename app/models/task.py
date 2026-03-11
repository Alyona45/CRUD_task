from sqlalchemy import Boolean, Column, Integer, String, Text

from app.models import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    is_done = Column(Boolean, nullable=False, default=False)
