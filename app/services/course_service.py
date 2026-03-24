from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.course import Course
from app.models.purchase import Purchase, PurchaseStatusEnum
from app.schemas.course import CourseCreate
from app.models.user import User, RoleEnum


def create_course(data: CourseCreate, current_user: User, db: Session) -> Course:
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


def get_all_courses(db: Session) -> list[Course]:
    return db.query(Course).filter(Course.is_published == True).all()


def get_course_by_id(course_id: int, db: Session) -> Course:
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


def update_course(course_id: int, data: CourseCreate, current_user: User, db: Session) -> Course:
    course = get_course_by_id(course_id, db)
    if course.author_id != current_user.id and current_user.role != RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Not allowed")
    course.title = data.title
    course.description = data.description
    course.price = data.price
    course.is_published = data.is_published
    db.commit()
    db.refresh(course)
    return course


def delete_course(course_id: int, current_user: User, db: Session):
    course = get_course_by_id(course_id, db)
    if course.author_id != current_user.id and current_user.role != RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Not allowed")
    db.delete(course)
    db.commit()


def check_purchase(course_id: int, user_id: int, db: Session) -> bool:
    purchase = db.query(Purchase).filter(
        Purchase.user_id == user_id,
        Purchase.course_id == course_id,
        Purchase.status == PurchaseStatusEnum.completed
    ).first()
    return purchase is not None