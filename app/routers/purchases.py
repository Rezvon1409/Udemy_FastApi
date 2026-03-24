from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.purchase import Purchase, PurchaseStatusEnum
from app.models.course import Course
from app.schemas.purchase import PurchaseCreate, PurchaseResponse
from app.routers.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/purchases", tags=["Purchases"])


@router.post("/", response_model=PurchaseResponse)
def buy_course(data: PurchaseCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    course = db.query(Course).filter(Course.id == data.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    existing = db.query(Purchase).filter(
        Purchase.user_id == current_user.id,
        Purchase.course_id == data.course_id,
        Purchase.status == PurchaseStatusEnum.completed
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Already purchased")
    purchase = Purchase(
        user_id=current_user.id,
        course_id=data.course_id,
        amount=course.price,
        status=PurchaseStatusEnum.completed
    )
    db.add(purchase)
    db.commit()
    db.refresh(purchase)
    return purchase


@router.get("/", response_model=list[PurchaseResponse])
def get_my_purchases(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Purchase).filter(Purchase.user_id == current_user.id).all()