from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Optional

from ..database import get_db
from ..services.lead_scoring_service import LeadScoringService
from ..services.recommendation_service import RecommendationService
from ..services.segmentation_service import SegmentationService
from ..services.nlp_service import NLPService
from ..services.analytics_service import AnalyticsService
from ..models.lead import Lead
from ..models.campaign import Campaign

router = APIRouter(
    prefix="/ai",
    tags=["AI Services"]
)

# Lead Scoring Endpoints
@router.post("/leads/{lead_id}/score")
async def score_lead(
    lead_id: int,
    db: Session = Depends(get_db)
):
    try:
        scoring_service = LeadScoringService()
        lead = db.query(Lead).filter(Lead.id == lead_id).first()
        if not lead:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Lead not found"
            )
        score = await scoring_service.score_lead(lead, db)
        return {"lead_id": lead_id, "score": score}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/leads/batch-score")
async def batch_score_leads(
    lead_ids: List[int],
    db: Session = Depends(get_db)
):
    try:
        scoring_service = LeadScoringService()
        leads = db.query(Lead).filter(Lead.id.in_(lead_ids)).all()
        scores = await scoring_service.batch_score_leads(leads, db)
        return {"scores": scores}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

# Recommendation Endpoints
@router.get("/leads/{lead_id}/recommendations/content")
async def get_content_recommendations(
    lead_id: int,
    limit: int = 5,
    db: Session = Depends(get_db)
):
    try:
        recommendation_service = RecommendationService()
        lead = db.query(Lead).filter(Lead.id == lead_id).first()
        if not lead:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Lead not found"
            )
        recommendations = await recommendation_service.get_content_recommendations(lead, limit, db)
        return {"recommendations": recommendations}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/leads/{lead_id}/recommendations/campaigns")
async def get_campaign_recommendations(
    lead_id: int,
    limit: int = 3,
    db: Session = Depends(get_db)
):
    try:
        recommendation_service = RecommendationService()
        lead = db.query(Lead).filter(Lead.id == lead_id).first()
        if not lead:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Lead not found"
            )
        recommendations = await recommendation_service.get_campaign_recommendations(lead, limit, db)
        return {"recommendations": recommendations}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

# Segmentation Endpoints
@router.post("/leads/{lead_id}/segment")
async def get_lead_segment(
    lead_id: int,
    db: Session = Depends(get_db)
):
    try:
        segmentation_service = SegmentationService()
        lead = db.query(Lead).filter(Lead.id == lead_id).first()
        if not lead:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Lead not found"
            )
        segment = await segmentation_service.get_lead_segment(lead, db)
        return {"lead_id": lead_id, "segment": segment}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/leads/batch-segment")
async def batch_segment_leads(
    lead_ids: List[int],
    db: Session = Depends(get_db)
):
    try:
        segmentation_service = SegmentationService()
        leads = db.query(Lead).filter(Lead.id.in_(lead_ids)).all()
        segments = await segmentation_service.batch_segment_leads(leads, db)
        return {"segments": segments}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

# NLP Endpoints
@router.post("/nlp/analyze-sentiment")
async def analyze_sentiment(
    text: str,
    db: Session = Depends(get_db)
):
    try:
        nlp_service = NLPService()
        sentiment = await nlp_service.analyze_sentiment(text)
        return sentiment
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/nlp/analyze-content")
async def analyze_content(
    text: str,
    db: Session = Depends(get_db)
):
    try:
        nlp_service = NLPService()
        analysis = await nlp_service.analyze_content(text)
        return analysis
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/nlp/generate-response")
async def generate_response(
    message: str,
    context: Dict[str, str],
    db: Session = Depends(get_db)
):
    try:
        nlp_service = NLPService()
        response = await nlp_service.generate_response(message, context)
        return {"response": response}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

# Analytics Endpoints
@router.get("/analytics/campaigns/{campaign_id}/performance")
async def get_campaign_performance(
    campaign_id: int,
    db: Session = Depends(get_db)
):
    try:
        analytics_service = AnalyticsService()
        campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
        if not campaign:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Campaign not found"
            )
        performance = await analytics_service.get_campaign_performance(campaign, db)
        return performance
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/analytics/campaigns/{campaign_id}/predict-performance")
async def predict_campaign_performance(
    campaign_id: int,
    days_ahead: int = 30,
    db: Session = Depends(get_db)
):
    try:
        analytics_service = AnalyticsService()
        campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
        if not campaign:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Campaign not found"
            )
        prediction = await analytics_service.predict_campaign_performance(campaign, days_ahead, db)
        return prediction
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/analytics/ab-test")
async def get_ab_test_results(
    campaign_a_id: int,
    campaign_b_id: int,
    db: Session = Depends(get_db)
):
    try:
        analytics_service = AnalyticsService()
        campaign_a = db.query(Campaign).filter(Campaign.id == campaign_a_id).first()
        campaign_b = db.query(Campaign).filter(Campaign.id == campaign_b_id).first()
        if not campaign_a or not campaign_b:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="One or both campaigns not found"
            )
        results = await analytics_service.get_ab_test_results(campaign_a, campaign_b, db)
        return results
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        ) 