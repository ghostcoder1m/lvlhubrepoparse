from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class WorkflowExecutionBase(BaseModel):
    workflow_id: int
    start_time: datetime
    end_time: Optional[datetime] = None
    status: str  # e.g., 'running', 'completed', 'failed'

class WorkflowExecutionCreate(WorkflowExecutionBase):
    pass

class WorkflowExecutionUpdate(WorkflowExecutionBase):
    pass

class WorkflowExecution(WorkflowExecutionBase):
    id: int

    class Config:
        orm_mode = True
