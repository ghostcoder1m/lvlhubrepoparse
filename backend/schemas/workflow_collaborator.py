from pydantic import BaseModel
from typing import Optional

class WorkflowCollaboratorBase(BaseModel):
    workflow_id: int
    user_id: int
    role: str  # e.g., "viewer", "editor"

class WorkflowCollaboratorCreate(WorkflowCollaboratorBase):
    pass

class WorkflowCollaboratorUpdate(WorkflowCollaboratorBase):
    pass

class WorkflowCollaborator(WorkflowCollaboratorBase):
    id: int

    class Config:
        orm_mode = True
