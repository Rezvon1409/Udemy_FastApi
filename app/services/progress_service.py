from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.progress import LessonProgress
from app.models.lesson import Lesson
from app.models.course import Course
from app.models.purchase import Purchase, PurchaseStatusEnum
from datetime import datetime


def mark_lesson_complete(lesson_id: int, user_id: int, db: Session) -> LessonProgress:
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    purchased = db.query(Purchase).filter(
        Purchase.user_id == user_id,
        Purchase.course_id == lesson.course_id,
        Purchase.status == PurchaseStatusEnum.completed
    ).first()
    if not purchased:
        raise HTTPException(status_code=403, detail="You must purchase this course first")

    existing = db.query(LessonProgress).filter(
        LessonProgress.user_id == user_id,
        LessonProgress.lesson_id == lesson_id
    ).first()
    if existing:
        existing.is_completed = True
        existing.completed_at = datetime.utcnow()
        db.commit()
        db.refresh(existing)
        return existing

    progress = LessonProgress(
        user_id=user_id,
        lesson_id=lesson_id,
        is_completed=True,
        completed_at=datetime.utcnow()
    )
    db.add(progress)
    db.commit()
    db.refresh(progress)
    return progress


def get_course_progress(course_id: int, user_id: int, db: Session) -> dict:
    lessons = db.query(Lesson).filter(Lesson.course_id == course_id).all()
    if not lessons:
        return {"total": 0, "completed": 0, "percent": 0}

    total = len(lessons)
    lesson_ids = [l.id for l in lessons]

    completed = db.query(LessonProgress).filter(
        LessonProgress.user_id == user_id,
        LessonProgress.lesson_id.in_(lesson_ids),
        LessonProgress.is_completed == True
    ).count()

    percent = round((completed / total) * 100)
    return {"total": total, "completed": completed, "percent": percent}