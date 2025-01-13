from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserItemInteractionBase(BaseModel):
    user_id: int
    item_id: int
    interaction_type: str  # e.g., 'viewed', 'clicked', 'purchased'
    timestamp: Optional[datetime] = None

class UserItemInteractionCreate(UserItemInteractionBase):
    pass

class UserItemInteraction(UserItemInteractionBase):
    id: int

    class Config:
        orm_mode = True
