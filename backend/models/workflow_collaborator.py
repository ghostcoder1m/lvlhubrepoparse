from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from ..database import Base

class WorkflowCollaborator(Base):
    __tablename__ = "workflow_collaborators"

    id = Column(Integer, primary_key=True, index=True)
    workflow_id = Column(Integer, ForeignKey("workflows.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    role = Column(String)  # e.g., "viewer", "editor"
    created_at = Column(DateTime)

    workflow = relationship("Workflow")
    user = relationship("User")

    def __init__(self, workflow_id, user_id, role, created_at):
        self.workflow_id = workflow_id
        self.user_id = user_id
        self.role = role
        self.created_at = created_at

    def __repr__(self):
        return f"<WorkflowCollaborator(id={self.id}, workflow_id={self.workflow_id}, user_id={self.user_id}, role='{self.role}')>"
