from sqlalchemy import Column, Integer, String, DateTime, Boolean
from ..database import Base

class AIModel(Base):
    __tablename__ = "aimodels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)  # e.g., "lead_scoring_model", "recommendation_model"
    version = Column(Integer)
    description = Column(String, nullable=True)
    model_type = Column(String)  # e.g., "logistic_regression", "random_forest"
    filepath = Column(String)  # Path to the serialized model file
    created_at = Column(DateTime)
    is_active = Column(Boolean)  # Indicates whether this version is currently active

    def __init__(self, name, version, description, model_type, filepath, created_at, is_active):
        self.name = name
        self.version = version
        self.description = description
        self.model_type = model_type
        self.filepath = filepath
        self.created_at = created_at
        self.is_active = is_active

    def __repr__(self):
        return f"<AIModel(id={self.id}, name='{self.name}', version={self.version}, is_active={self.is_active})>"
