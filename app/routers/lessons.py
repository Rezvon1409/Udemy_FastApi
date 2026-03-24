from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.lesson import Lesson
from app.models.course import Course
from app.schemas.lesson import LessonCreate, LessonResponse
from app.routers.auth import get_current_user
from app.models.user import User, RoleEnum

router = APIRouter(prefix="/lessons", tags=["Lessons"])


@router.post("/{course_id}", response_model=LessonResponse)
def create_lesson(course_id: int, data: LessonCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    if course.author_id != current_user.id and current_user.role != RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Not allowed")
    lesson = Lesson(
        course_id=course_id,
        title=data.title,
        video_url=data.video_url,
        content=data.content,
        order=data.order
    )
    db.add(lesson)
    db.commit()
    db.refresh(lesson)
    return lesson


@router.get("/{course_id}", response_model=list[LessonResponse])
def get_lessons(course_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return db.query(Lesson).filter(Lesson.course_id == course_id).order_by(Lesson.order).all()


@router.put("/{lesson_id}", response_model=LessonResponse)
def update_lesson(lesson_id: int, data: LessonCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    course = db.query(Course).filter(Course.id == lesson.course_id).first()
    if course.author_id != current_user.id and current_user.role != RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Not allowed")
    lesson.title = data.title
    lesson.video_url = data.video_url
    lesson.content = data.content
    lesson.order = data.order
    db.commit()
    db.refresh(lesson)
    return lesson


@router.delete("/{lesson_id}")
def delete_lesson(lesson_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    course = db.query(Course).filter(Course.id == lesson.course_id).first()
    if course.author_id != current_user.id and current_user.role != RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Not allowed")
    db.delete(lesson)
    db.commit()
    return {"message": "Lesson deleted"}