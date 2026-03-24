from pydantic import BaseModel
from app.models.task import TaskTypeEnum


class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    task_type: TaskTypeEnum


class TaskResponse(BaseModel):
    id: int
    lesson_id: int
    title: str
    description: str | None
    task_type: TaskTypeEnum

    class Config:
        from_attributes = True