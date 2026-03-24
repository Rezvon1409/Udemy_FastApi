from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.course import Course
from app.schemas.course import CourseCreate, CourseResponse
from app.routers.auth import get_current_user
from app.models.user import User, RoleEnum

router = APIRouter(prefix="/courses", tags=["Courses"])


@router.post("/", response_model=CourseResponse)
def create_course(data: CourseCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != RoleEnum.author and current_user.role != RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Not allowed")
    course = Course(
        author_id=current_user.id,
        title=data.title,
        description=data.description,
        price=data.price,
        is_published=data.is_published
    )
    db.add(course)
    db.commit()
    db.refresh(course)
    return course


@router.get("/", response_model=list[CourseResponse])
def get_courses(db: Session = Depends(get_db)):
    return db.query(Course).filter(Course.is_published == True).all()


@router.get("/{course_id}", response_model=CourseResponse)
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@router.put("/{course_id}", response_model=CourseResponse)
def update_course(course_id: int, data: CourseCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    if course.author_id != current_user.id and current_user.role != RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Not allowed")
    course.title = data.title
    course.description = data.description
    course.price = data.price
    course.is_published = data.is_published
    db.commit()
    db.refresh(course)
    return course


@router.delete("/{course_id}")
def delete_course(course_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    if course.author_id != current_user.id and current_user.role != RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Not allowed")
    db.delete(course)
    db.commit()
    return {"message": "Course deleted"}