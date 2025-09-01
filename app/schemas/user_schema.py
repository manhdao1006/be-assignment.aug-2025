from pydantic import BaseModel, EmailStr
from typing import Optional
from app.models.user import RoleEnum

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    role: Optional[RoleEnum] = None

class UserRegister(UserBase):
    password: str

class UserCreate(UserBase):
    password: str
    organization_id: int
    
class UserUpdate(UserBase):
    organization_id: int

class UserOut(UserBase):
    id: int
    organization_id: Optional[int] = None

    class Config:
        orm_mode = True
