from pydantic import BaseModel, EmailStr
from app.models.user import RoleEnum


class UserRegister(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    role: RoleEnum = RoleEnum.student


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    role: RoleEnum

    class Config:
        from_attributes = True