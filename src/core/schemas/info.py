from typing import Optional
from pydantic import BaseModel


class InfoBase(BaseModel):
    foo: Optional[int] = None
    baz: Optional[int] = None
    
class InfoCreate(InfoBase):
    user_id : int

class InfoRead(InfoBase):
    user_id : int
    id : int

class InfoUpdate(InfoBase):
    pass

class InfoDelete(BaseModel):
    deleted : int