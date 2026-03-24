from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.routers.auth import get_current_user
from app.models.user import User
from app.services.progress_service import mark_lesson_complete, get_course_progress

router = APIRouter(prefix="/progress", tags=["Progress"])


@router.post("/{lesson_id}")
def complete_lesson(lesson_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return mark_lesson_complete(lesson_id, current_user.id, db)


@router.get("/{course_id}")
def course_progress(course_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_course_progress(course_id, current_user.id, db)