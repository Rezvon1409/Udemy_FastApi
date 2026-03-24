from pydantic import BaseModel
from decimal import Decimal


class CourseCreate(BaseModel):
    title: str
    description: str | None = None
    price: Decimal = 0
    is_published: bool = False


class CourseResponse(BaseModel):
    id: int
    author_id: int
    title: str
    description: str | None
    price: Decimal
    is_published: bool

    class Config:
        from_attributes = True