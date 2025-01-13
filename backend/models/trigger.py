from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class Trigger(Base):
    __tablename__ = "triggers"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)  # e.g., 'email_opened', 'link_clicked', 'form_submitted'
    workflow_id = Column(Integer, ForeignKey("workflows.id"))

    workflow = relationship("Workflow", back_populates="triggers")

    def __init__(self, type, workflow_id):
        self.type = type
        self.workflow_id = workflow_id

    def __repr__(self):
        return f"<Trigger(id={self.id}, type='{self.type}')>"
