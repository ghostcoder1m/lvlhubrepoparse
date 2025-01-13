from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime

class ModelVersionBase(BaseModel):
    model_type: str = Field(..., description="Type of the model (lead_scoring, recommendation, etc.)")
    version: str = Field(..., description="Version identifier of the model")
    endpoint_id: str = Field(..., description="Vertex AI endpoint ID")
    description: Optional[str] = Field(None, description="Description of the model version")
    parameters: Optional[Dict[str, Any]] = Field(None, description="Model parameters and configuration")

class ModelVersionCreate(ModelVersionBase):
    pass

class ModelVersionUpdate(BaseModel):
    description: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None

class ModelVersionResponse(ModelVersionBase):
    id: int
    created_at: datetime
    is_active: bool

    class Config:
        from_attributes = True

class PredictionBase(BaseModel):
    model_version_id: int = Field(..., description="ID of the model version used")
    prediction_type: str = Field(..., description="Type of prediction made")
    input_data: Dict[str, Any] = Field(..., description="Input data for the prediction")
    output_data: Dict[str, Any] = Field(..., description="Output data from the prediction")
    confidence_score: Optional[float] = Field(None, description="Confidence score of the prediction")

class PredictionCreate(PredictionBase):
    pass

class PredictionResponse(PredictionBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class PerformanceMetricBase(BaseModel):
    model_version_id: int = Field(..., description="ID of the model version")
    metric_name: str = Field(..., description="Name of the metric")
    metric_value: float = Field(..., description="Value of the metric")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional metric details")

class PerformanceMetricCreate(PerformanceMetricBase):
    pass

class PerformanceMetricResponse(PerformanceMetricBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True

class ABTestBase(BaseModel):
    campaign_a_id: int = Field(..., description="ID of the first campaign")
    campaign_b_id: int = Field(..., description="ID of the second campaign")
    start_date: datetime = Field(..., description="Start date of the A/B test")
    end_date: Optional[datetime] = Field(None, description="End date of the A/B test")
    metrics: Optional[Dict[str, Any]] = Field(None, description="Test metrics and results")
    winner: Optional[str] = Field(None, description="Winner of the test (A, B, or tie)")
    confidence_level: Optional[float] = Field(None, description="Statistical confidence level")

class ABTestCreate(ABTestBase):
    pass

class ABTestUpdate(BaseModel):
    end_date: Optional[datetime] = None
    metrics: Optional[Dict[str, Any]] = None
    winner: Optional[str] = None
    confidence_level: Optional[float] = None

class ABTestResponse(ABTestBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Additional schemas for specific AI service responses
class LeadScoreResponse(BaseModel):
    lead_id: int
    score: float
    confidence: float
    factors: List[Dict[str, Any]]
    timestamp: datetime

class ContentRecommendation(BaseModel):
    content_id: int
    content_type: str
    relevance_score: float
    reason: str

class ContentRecommendationsResponse(BaseModel):
    lead_id: int
    recommendations: List[ContentRecommendation]
    timestamp: datetime

class CampaignRecommendation(BaseModel):
    campaign_id: int
    relevance_score: float
    expected_conversion_rate: float
    reason: str

class CampaignRecommendationsResponse(BaseModel):
    lead_id: int
    recommendations: List[CampaignRecommendation]
    timestamp: datetime

class SegmentResponse(BaseModel):
    lead_id: int
    segment: str
    confidence: float
    factors: List[Dict[str, Any]]
    timestamp: datetime

class SentimentAnalysisResponse(BaseModel):
    text: str
    sentiment: str
    confidence: float
    scores: Dict[str, float]
    timestamp: datetime

class ContentAnalysisResponse(BaseModel):
    text: str
    topics: List[str]
    keywords: List[str]
    entities: List[Dict[str, Any]]
    summary: str
    timestamp: datetime

class CampaignPerformanceResponse(BaseModel):
    campaign_id: int
    metrics: Dict[str, Any]
    trends: Dict[str, List[float]]
    insights: List[str]
    timestamp: datetime

class PerformancePredictionResponse(BaseModel):
    campaign_id: int
    predicted_metrics: Dict[str, Any]
    confidence_intervals: Dict[str, Dict[str, float]]
    factors: List[Dict[str, Any]]
    timestamp: datetime 