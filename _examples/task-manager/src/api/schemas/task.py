from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, examples=["Buy groceries"])
    description: str = Field(default="", max_length=2000, examples=["Milk, eggs, bread"])


class TaskStatusUpdate(BaseModel):
    status: str = Field(..., pattern="^(todo|in_progress|done)$", examples=["in_progress"])


class TaskResponse(BaseModel):
    id: UUID
    title: str
    description: str
    status: str
    created_at: datetime
    updated_at: datetime


class TaskListResponse(BaseModel):
    count: int
    tasks: list[TaskResponse]
