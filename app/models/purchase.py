from sqlalchemy import Column, Integer, DECIMAL, TIMESTAMP, ForeignKey, Enum
from sqlalchemy.sql import func
from app.database import Base
import enum
from sqlalchemy.orm import relationship

class PurchaseStatusEnum(str, enum.Enum):
    pending = "pending"
    completed = "completed"
    failed = "failed"


class Purchase(Base):
    __tablename__ = "purchases"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    amount = Column(DECIMAL, nullable=False)
    status = Column(Enum(PurchaseStatusEnum), default=PurchaseStatusEnum.pending)
    purchased_at = Column(TIMESTAMP, server_default=func.now())


    user = relationship("User", back_populates="purchases")
    course = relationship("Course", back_populates="purchases")