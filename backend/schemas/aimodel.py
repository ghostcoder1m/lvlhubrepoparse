from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AIModelBase(BaseModel):
    name: str
    version: int
    model_type: str  # e.g., "logistic_regression", "random_forest"
    filepath: str  # Path to the serialized model file
    description: Optional[str] = None
    created_at: datetime
    is_active: bool  # Indicates whether this version is currently active

class AIModelCreate(AIModelBase):
    pass

class AIModelUpdate(AIModelBase):
    pass

class AIModel(AIModelBase):
    id: int

    class Config:
        orm_mode = True
