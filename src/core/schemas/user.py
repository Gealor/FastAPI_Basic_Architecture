from typing import Optional
from pydantic import BaseModel
from pydantic import EmailStr

class UserBase(BaseModel):
    username: str
    mail: EmailStr
    password: str

class UserCreate(UserBase):
    pass

class UserRead(UserBase):
    id: int

class UserDelete(BaseModel):
    deleted : int

class UserNameMail(BaseModel):
    username: str
    mail: str
