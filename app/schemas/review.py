from pydantic import BaseModel


class ReviewCreate(BaseModel):
    rating: int
    comment: str | None = None


class ReviewResponse(BaseModel):
    id: int
    course_id: int
    user_id: int
    rating: int
    comment: str | None

    class Config:
        from_attributes = True