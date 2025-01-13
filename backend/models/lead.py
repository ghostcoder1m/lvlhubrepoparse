from sqlalchemy import Column, Integer, String, DateTime, JSON, Float
from sqlalchemy.orm import relationship
from ..database import Base
from datetime import datetime

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    company = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    source = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    lead_score = Column(Float, default=0.0)
    data = Column(JSON, default=dict)

    # Relationships
    events = relationship("Event", back_populates="lead", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Lead(id={self.id}, email='{self.email}', first_name='{self.first_name}', last_name='{self.last_name}', company='{self.company}')>"
