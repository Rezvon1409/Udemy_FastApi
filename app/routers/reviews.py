from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.review import Review
from app.models.purchase import Purchase, PurchaseStatusEnum
from app.schemas.review import ReviewCreate, ReviewResponse
from app.routers.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/reviews", tags=["Reviews"])


@router.post("/{course_id}", response_model=ReviewResponse)
def create_review(course_id: int, data: ReviewCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    purchased = db.query(Purchase).filter(
        Purchase.user_id == current_user.id,
        Purchase.course_id == course_id,
        Purchase.status == PurchaseStatusEnum.completed
    ).first()
    if not purchased:
        raise HTTPException(status_code=403, detail="You must purchase this course first")
    existing = db.query(Review).filter(
        Review.user_id == current_user.id,
        Review.course_id == course_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Already reviewed")
    if data.rating < 1 or data.rating > 5:
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")
    review = Review(
        course_id=course_id,
        user_id=current_user.id,
        rating=data.rating,
        comment=data.comment
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return review


@router.get("/{course_id}", response_model=list[ReviewResponse])
def get_reviews(course_id: int, db: Session = Depends(get_db)):
    return db.query(Review).filter(Review.course_id == course_id).all()


@router.delete("/{review_id}")
def delete_review(review_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    if review.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")
    db.delete(review)
    db.commit()
    return {"message": "Review deleted"}