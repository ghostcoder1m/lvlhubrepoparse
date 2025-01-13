from pydantic import BaseModel
from typing import Optional

class ActionBase(BaseModel):
    type: str  # e.g., 'send_email', 'update_lead', 'add_to_campaign'
    trigger_id: int

class ActionCreate(ActionBase):
    pass

class ActionUpdate(ActionBase):
    pass

class Action(ActionBase):
    id: int

    class Config:
        orm_mode = True
