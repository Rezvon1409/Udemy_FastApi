from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.task import Task
from app.models.lesson import Lesson
from app.models.course import Course
from app.schemas.task import TaskCreate, TaskResponse
from app.routers.auth import get_current_user
from app.models.user import User, RoleEnum

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/{lesson_id}", response_model=TaskResponse)
def create_task(lesson_id: int, data: TaskCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    course = db.query(Course).filter(Course.id == lesson.course_id).first()
    if course.author_id != current_user.id and current_user.role != RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Not allowed")
    task = Task(
        lesson_id=lesson_id,
        title=data.title,
        description=data.description,
        task_type=data.task_type
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.get("/{lesson_id}", response_model=list[TaskResponse])
def get_tasks(lesson_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return db.query(Task).filter(Task.lesson_id == lesson_id).all()


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, data: TaskCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    lesson = db.query(Lesson).filter(Lesson.id == task.lesson_id).first()
    course = db.query(Course).filter(Course.id == lesson.course_id).first()
    if course.author_id != current_user.id and current_user.role != RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Not allowed")
    task.title = data.title
    task.description = data.description
    task.task_type = data.task_type
    db.commit()
    db.refresh(task)
    return task


@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    lesson = db.query(Lesson).filter(Lesson.id == task.lesson_id).first()
    course = db.query(Course).filter(Course.id == lesson.course_id).first()
    if course.author_id != current_user.id and current_user.role != RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Not allowed")
    db.delete(task)
    db.commit()
    return {"message": "Task deleted"}