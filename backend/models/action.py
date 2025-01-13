from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class Action(Base):
    __tablename__ = "actions"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)  # e.g., 'send_email', 'update_lead', 'add_to_campaign'
    trigger_id = Column(Integer, ForeignKey("triggers.id"))

    trigger = relationship("Trigger", back_populates="actions")

    def __init__(self, type, trigger_id):
        self.type = type
        self.trigger_id = trigger_id

    def __repr__(self):
        return f"<Action(id={self.id}, type='{self.type}')>"
