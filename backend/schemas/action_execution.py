from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ActionExecutionBase(BaseModel):
    workflow_execution_id: int
    action_id: int
    start_time: datetime
    end_time: Optional[datetime] = None
    status: str  # e.g., 'running', 'completed', 'failed'
    result: Optional[str] = None  # For storing action execution output, errors, or other details.

class ActionExecutionCreate(ActionExecutionBase):
    pass

class ActionExecutionUpdate(ActionExecutionBase):
    pass

class ActionExecution(ActionExecutionBase):
    id: int

    class Config:
        orm_mode = True
