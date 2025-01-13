from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    type = Column(String(50), nullable=False)
    status = Column(String(20), default="draft")
    target_audience = Column(String(200))
    budget = Column(Float)
    
    # Timestamps
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_modified_at = Column(DateTime, onupdate=datetime.utcnow)
    launched_at = Column(DateTime)
    
    # User relationships
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    last_modified_by = Column(Integer, ForeignKey("users.id"))
    launched_by = Column(Integer, ForeignKey("users.id"))
    
    # Relationships
    creator = relationship("User", foreign_keys=[created_by], back_populates="created_campaigns")
    modifier = relationship("User", foreign_keys=[last_modified_by], back_populates="modified_campaigns")
    launcher = relationship("User", foreign_keys=[launched_by], back_populates="launched_campaigns")
    leads = relationship("Lead", back_populates="campaign")
    
    # Stats
    leads_count = Column(Integer, default=0)
    conversion_rate = Column(Float, default=0.0)

    def __repr__(self):
        return f"<Campaign {self.name}>"
