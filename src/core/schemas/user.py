from typing import Optional
from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    mail: str
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
