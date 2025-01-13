from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MessageBase(BaseModel):
    content: str
    sent_at: datetime
    status: Optional[str] = "sent"  # e.g., 'sent', 'failed', 'delivered'

class MessageCreate(MessageBase):
    pass

class MessageUpdate(MessageBase):
    pass

class Message(MessageBase):
    id: int

    class Config:
        orm_mode = True
