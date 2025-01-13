from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from ..database import Base

class WorkflowExecution(Base):
    __tablename__ = "workflow_executions"

    id = Column(Integer, primary_key=True, index=True)
    workflow_id = Column(Integer, ForeignKey("workflows.id"))
    start_time = Column(DateTime)
    end_time = Column(DateTime, nullable=True)
    status = Column(String)  # e.g., 'running', 'completed', 'failed'

    def __init__(self, workflow_id, start_time, end_time=None, status='running'):
        self.workflow_id = workflow_id
        self.start_time = start_time
        self.end_time = end_time
        self.status = status

    def __repr__(self):
        return f"<WorkflowExecution(id={self.id}, workflow_id={self.workflow_id}, status='{self.status}')>"
