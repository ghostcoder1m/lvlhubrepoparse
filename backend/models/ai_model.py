from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

class AIModel(Base):
    __tablename__ = "ai_models"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)  # e.g., "lead_scoring", "recommendation"
    version = Column(Integer)
    description = Column(Text, nullable=True)
    model_type = Column(String)  # e.g., "random_forest", "neural_network"
    filepath = Column(String)  # path to serialized model
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=False)
    metrics = Column(Text, nullable=True)  # JSON string of model metrics
    parameters = Column(Text, nullable=True)  # JSON string of model parameters

    class Config:
        from_attributes = True

    def __repr__(self):
        return f"<AIModel(name='{self.name}', version={self.version}, type='{self.model_type}', active={self.is_active})>" 