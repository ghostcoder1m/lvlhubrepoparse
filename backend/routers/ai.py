from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import json

from ..database import get_db
from ..services.lead_scoring_service import LeadScoringService
from ..services.recommendation_service import RecommendationService
from ..models.lead import Lead
from ..models.ai_model import AIModel

router = APIRouter()

@router.post("/ai/leads/{lead_id}/score")
def score_lead(lead_id: int, db: Session = Depends(get_db)):
    """Score a lead using the active lead scoring model."""
    # Get lead
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
        
    # Score lead
    scoring_service = LeadScoringService(db)
    score = scoring_service.score_lead(lead)
    
    if score is None:
        raise HTTPException(status_code=400, detail="No active lead scoring model found")
        
    # Update lead score
    lead.lead_score = score
    db.commit()
    
    # Get feature importance for explanation
    feature_importance = scoring_service.get_feature_importance()
    
    return {
        "lead_id": lead_id,
        "score": score,
        "feature_importance": feature_importance,
        "explanation": _generate_score_explanation(score, feature_importance)
    }

@router.post("/ai/leads/{lead_id}/recommendations")
def get_recommendations(
    lead_id: int,
    n_recommendations: int = 5,
    db: Session = Depends(get_db)
):
    """Get personalized recommendations for a lead."""
    # Get lead
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
        
    # Get recommendations
    recommendation_service = RecommendationService(db)
    recommendations = recommendation_service.get_recommendations(
        lead,
        n_recommendations=n_recommendations
    )
    
    if not recommendations:
        raise HTTPException(status_code=400, detail="No active recommendation model found")
        
    return recommendations

@router.post("/ai/models/lead-scoring/train")
def train_lead_scoring_model(
    training_data: List[Dict[str, Any]],
    db: Session = Depends(get_db)
):
    """Train a new lead scoring model."""
    scoring_service = LeadScoringService(db)
    metrics = scoring_service.train_model(training_data)
    
    return {
        "message": "Lead scoring model trained successfully",
        "metrics": metrics
    }

@router.post("/ai/models/recommendations/train")
def train_recommendation_model(db: Session = Depends(get_db)):
    """Train a new recommendation model."""
    # Get all leads for training
    leads = db.query(Lead).all()
    if not leads:
        raise HTTPException(status_code=400, detail="No leads available for training")
        
    recommendation_service = RecommendationService(db)
    metrics = recommendation_service.train_model(leads)
    
    return {
        "message": "Recommendation model trained successfully",
        "metrics": metrics
    }

@router.get("/ai/models")
def list_models(db: Session = Depends(get_db)):
    """List all AI models."""
    models = db.query(AIModel).all()
    return [
        {
            "id": model.id,
            "name": model.name,
            "version": model.version,
            "description": model.description,
            "model_type": model.model_type,
            "created_at": model.created_at,
            "is_active": model.is_active,
            "metrics": json.loads(model.metrics) if model.metrics else None
        }
        for model in models
    ]

@router.post("/ai/models/{model_id}/activate")
def activate_model(model_id: int, db: Session = Depends(get_db)):
    """Activate a specific model version."""
    # Get model
    model = db.query(AIModel).filter(AIModel.id == model_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
        
    # Deactivate other models of the same type
    db.query(AIModel).filter(
        AIModel.name == model.name,
        AIModel.is_active == True
    ).update({"is_active": False})
    
    # Activate selected model
    model.is_active = True
    db.commit()
    
    return {"message": f"Model {model.name} v{model.version} activated successfully"}

def _generate_score_explanation(score: float, feature_importance: Dict[str, float]) -> str:
    """Generate a human-readable explanation for a lead score."""
    # Sort features by importance
    sorted_features = sorted(
        feature_importance.items(),
        key=lambda x: x[1],
        reverse=True
    )[:3]  # Get top 3 features
    
    # Generate explanation
    if score >= 0.8:
        quality = "excellent"
    elif score >= 0.6:
        quality = "good"
    elif score >= 0.4:
        quality = "moderate"
    else:
        quality = "low"
        
    explanation = f"This lead has a {quality} likelihood of conversion. "
    explanation += "This is based primarily on "
    
    feature_explanations = []
    for feature, importance in sorted_features:
        if feature == 'total_events':
            feature_explanations.append("overall engagement level")
        elif feature == 'form_submissions':
            feature_explanations.append("number of form submissions")
        elif feature == 'page_views':
            feature_explanations.append("website activity")
        elif feature == 'resource_downloads':
            feature_explanations.append("downloaded resources")
        elif feature == 'company_size':
            feature_explanations.append("company size")
        elif feature == 'has_company':
            feature_explanations.append("provided company information")
        elif feature == 'has_phone':
            feature_explanations.append("provided contact details")
            
    explanation += ", ".join(feature_explanations)
    
    return explanation 