from pydantic import BaseModel
from decimal import Decimal
from app.models.purchase import PurchaseStatusEnum


class PurchaseCreate(BaseModel):
    course_id: int


class PurchaseResponse(BaseModel):
    id: int
    user_id: int
    course_id: int
    amount: Decimal
    status: PurchaseStatusEnum

    class Config:
        from_attributes = True