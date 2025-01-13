from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

from ..database import Base

class ModelVersion(Base):
    __tablename__ = "model_versions"

    id = Column(Integer, primary_key=True, index=True)
    model_type = Column(String, nullable=False)  # lead_scoring, recommendation, segmentation, nlp, analytics
    version = Column(String, nullable=False)
    endpoint_id = Column(String, nullable=False)
    description = Column(String)
    parameters = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    predictions = relationship("Prediction", back_populates="model_version")

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    model_version_id = Column(Integer, ForeignKey("model_versions.id"))
    prediction_type = Column(String, nullable=False)  # score, recommendation, segment, sentiment, performance
    input_data = Column(JSON)
    output_data = Column(JSON)
    confidence_score = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    model_version = relationship("ModelVersion", back_populates="predictions")

class PerformanceMetric(Base):
    __tablename__ = "performance_metrics"

    id = Column(Integer, primary_key=True, index=True)
    model_version_id = Column(Integer, ForeignKey("model_versions.id"))
    metric_name = Column(String, nullable=False)  # accuracy, precision, recall, f1, etc.
    metric_value = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    details = Column(JSON)

class ABTest(Base):
    __tablename__ = "ab_tests"

    id = Column(Integer, primary_key=True, index=True)
    campaign_a_id = Column(Integer, ForeignKey("campaigns.id"))
    campaign_b_id = Column(Integer, ForeignKey("campaigns.id"))
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime)
    metrics = Column(JSON)  # Store various test metrics
    winner = Column(String)  # 'A', 'B', or 'tie'
    confidence_level = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    campaign_a = relationship("Campaign", foreign_keys=[campaign_a_id])
    campaign_b = relationship("Campaign", foreign_keys=[campaign_b_id]) 