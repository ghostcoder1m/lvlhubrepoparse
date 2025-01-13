from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class Workflow(Base):
    __tablename__ = "workflows"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    is_active = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="workflows")
    triggers = relationship("Trigger", back_populates="workflow")
    actions = relationship("Action", back_populates="workflow")

    def __init__(self, name, description, is_active, user_id):
        self.name = name
        self.description = description
        self.is_active = is_active
        self.user_id = user_id

    def __repr__(self):
        return f"<Workflow(id={self.id}, name='{self.name}', is_active={self.is_active})>"
