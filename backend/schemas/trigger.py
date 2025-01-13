from pydantic import BaseModel
from typing import Optional

class TriggerBase(BaseModel):
    type: str  # e.g., 'email_opened', 'link_clicked', 'form_submitted'
    workflow_id: int

class TriggerCreate(TriggerBase):
    pass

class TriggerUpdate(TriggerBase):
    pass

class Trigger(TriggerBase):
    id: int

    class Config:
        orm_mode = True
