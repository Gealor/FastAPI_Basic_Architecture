from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
from pydantic import EmailStr

class UserBase(BaseModel):
    username: str
    mail: EmailStr
    password: str

class UserCreate(UserBase):
    pass

class UserRead(UserBase):
    id: int
    created_at: datetime

class UserUpdate(BaseModel):
    username: Optional[str] = None
    mail: Optional[EmailStr] = None
    password: Optional[str] = None

class UserDelete(BaseModel):
    deleted : int

class UserNameMail(BaseModel):
    username: str
    mail: str
