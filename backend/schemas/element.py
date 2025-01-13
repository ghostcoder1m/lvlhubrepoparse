from pydantic import BaseModel
from typing import Optional

class ElementBase(BaseModel):
    type: str  # e.g., 'text', 'image', 'button'
    content: str

class ElementCreate(ElementBase):
    pass

class ElementUpdate(ElementBase):
    pass

class Element(ElementBase):
    id: int

    class Config:
        orm_mode = True
