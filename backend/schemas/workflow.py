from pydantic import BaseModel
from typing import Optional

class WorkflowBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_active: Optional[bool] = False
    user_id: int

class WorkflowCreate(WorkflowBase):
    pass

class WorkflowUpdate(WorkflowBase):
    pass

class Workflow(WorkflowBase):
    id: int

    class Config:
        orm_mode = True
