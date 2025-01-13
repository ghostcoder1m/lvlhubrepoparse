from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from ..database import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String, index=True)
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=True)
    source = Column(String)
    properties = Column(JSON)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    lead = relationship("Lead", back_populates="events") 