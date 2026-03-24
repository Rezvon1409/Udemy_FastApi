from pydantic import BaseModel


class LessonCreate(BaseModel):
    title: str
    video_url: str | None = None
    content: str | None = None
    order: int = 0


class LessonResponse(BaseModel):
    id: int
    course_id: int
    title: str
    video_url: str | None
    content: str | None
    order: int

    class Config:
        from_attributes = True