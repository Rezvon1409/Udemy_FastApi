from pydantic import BaseModel , EmailStr
from app.models.user import *


class UserRegister(BaseModel):
    email : EmailStr
    password : str
    full_name : str

class UserLogin(BaseModel):
    email :EmailStr
    password : str


class UserResponse(BaseModel):
    id : int
    email : str
    full_name : str
    role :RoleEnum

    class Config:
        from_attributes = True