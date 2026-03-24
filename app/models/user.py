from sqlalchemy import Column , Integer , String , Enum , TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum

class RoleEnum(str , enum.Enum):
    student = 'student'
    author = 'author'
    admin = 'admin'

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer , primary_key=True , index=True)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    role = Column(Enum(RoleEnum), default=RoleEnum.student)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    courses = relationship("Course", back_populates="author")
