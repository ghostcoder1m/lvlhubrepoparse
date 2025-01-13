import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from sqlalchemy import func
from sqlalchemy.orm import Session

from .ai_service import AIService
from ..models.campaign import Campaign
from ..models.lead import Lead
from ..models.user_item_interaction import UserItemInteraction
from ..config.ai_config import MODEL_PARAMETERS, FEATURE_ENGINEERING

class AnalyticsService:
    def __init__(self):
        self.ai_service = AIService()
        self.performance_endpoint_id = self.ai_service.get_endpoint_id("performance")
        self.config = MODEL_PARAMETERS["analytics"]
        self.feature_config = FEATURE_ENGINEERING

    def _calculate_campaign_metrics(self, campaign: Campaign, db: Session) -> Dict[str, Any]:
        """Calculate core metrics for a campaign"""
        now = datetime.utcnow()
        
        # Get all interactions for the campaign
        interactions = db.query(UserItemInteraction).filter(
            UserItemInteraction.campaign_id == campaign.id
        ).all()
        
        # Calculate metrics
        total_interactions = len(interactions)
        unique_leads = len(set(i.lead_id for i in interactions))
        
        # Group interactions by type
        interaction_types = {}
        for interaction in interactions:
            if interaction.type not in interaction_types:
                interaction_types[interaction.type] = 0
            interaction_types[interaction.type] += 1
            
        # Calculate engagement rate
        engagement_rate = total_interactions / unique_leads if unique_leads > 0 else 0
        
        # Calculate conversion rate
        conversions = sum(1 for i in interactions if i.type == "conversion")
        conversion_rate = conversions / unique_leads if unique_leads > 0 else 0
        
        return {
            "total_interactions": total_interactions,
            "unique_leads": unique_leads,
            "interaction_types": interaction_types,
            "engagement_rate": engagement_rate,
            "conversion_rate": conversion_rate,
            "timestamp": now
        }

    def _prepare_performance_features(self, campaign: Campaign, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare features for performance prediction"""
        return {
            "campaign_id": campaign.id,
            "campaign_type": campaign.type,
            "target_audience": campaign.target_audience,
            "budget": campaign.budget,
            "duration": (campaign.end_date - campaign.start_date).days if campaign.end_date else None,
            "total_interactions": metrics["total_interactions"],
            "unique_leads": metrics["unique_leads"],
            "engagement_rate": metrics["engagement_rate"],
            "conversion_rate": metrics["conversion_rate"],
            "interaction_types": metrics["interaction_types"],
            "timestamp": datetime.utcnow().isoformat()
        }

    async def get_campaign_performance(self, campaign_id: int, db: Session) -> Dict[str, Any]:
        """Get performance metrics for a campaign"""
        try:
            campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
            if not campaign:
                raise ValueError(f"Campaign {campaign_id} not found")
                
            metrics = self._calculate_campaign_metrics(campaign, db)
            
            return {
                "campaign_id": campaign_id,
                "metrics": metrics,
                "status": campaign.status,
                "start_date": campaign.start_date,
                "end_date": campaign.end_date,
                "timestamp": datetime.utcnow()
            }
            
        except Exception as e:
            logging.error(f"Failed to get campaign performance: {str(e)}")
            raise

    async def predict_campaign_performance(self, campaign_id: int, db: Session) -> Dict[str, Any]:
        """Predict future performance of a campaign"""
        try:
            campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
            if not campaign:
                raise ValueError(f"Campaign {campaign_id} not found")
                
            # Get current metrics
            current_metrics = self._calculate_campaign_metrics(campaign, db)
            
            # Prepare features for prediction
            features = self._prepare_performance_features(campaign, current_metrics)
            
            # Get prediction
            prediction = await self.ai_service.predict(
                self.performance_endpoint_id,
                instances=[features]
            )
            
            result = prediction[0]
            if result["confidence"] < self.config["prediction_threshold"]:
                logging.warning(f"Low confidence performance prediction: {result['confidence']}")
            
            return {
                "campaign_id": campaign_id,
                "current_metrics": current_metrics,
                "predicted_metrics": {
                    "expected_interactions": result["expected_interactions"],
                    "expected_conversions": result["expected_conversions"],
                    "expected_engagement_rate": result["expected_engagement_rate"],
                    "expected_conversion_rate": result["expected_conversion_rate"],
                    "growth_trajectory": result["growth_trajectory"]
                },
                "confidence": result["confidence"],
                "factors": result["contributing_factors"],
                "recommendations": result["recommendations"],
                "timestamp": datetime.utcnow()
            }
            
        except Exception as e:
            logging.error(f"Failed to predict campaign performance: {str(e)}")
            raise

    async def get_lead_analytics(self, lead_id: int, db: Session) -> Dict[str, Any]:
        """Get analytics for a specific lead"""
        try:
            lead = db.query(Lead).filter(Lead.id == lead_id).first()
            if not lead:
                raise ValueError(f"Lead {lead_id} not found")
                
            # Get all interactions for the lead
            interactions = db.query(UserItemInteraction).filter(
                UserItemInteraction.lead_id == lead_id
            ).order_by(UserItemInteraction.timestamp.desc()).all()
            
            # Calculate engagement metrics
            total_interactions = len(interactions)
            interaction_types = {}
            campaigns_engaged = set()
            
            for interaction in interactions:
                if interaction.type not in interaction_types:
                    interaction_types[interaction.type] = 0
                interaction_types[interaction.type] += 1
                
                if interaction.campaign_id:
                    campaigns_engaged.add(interaction.campaign_id)
            
            # Calculate time-based metrics
            if interactions:
                first_interaction = min(i.timestamp for i in interactions)
                last_interaction = max(i.timestamp for i in interactions)
                engagement_duration = (last_interaction - first_interaction).days
            else:
                engagement_duration = 0
            
            return {
                "lead_id": lead_id,
                "total_interactions": total_interactions,
                "interaction_types": interaction_types,
                "campaigns_engaged": len(campaigns_engaged),
                "engagement_duration": engagement_duration,
                "first_interaction": first_interaction if interactions else None,
                "last_interaction": last_interaction if interactions else None,
                "current_score": lead.score,
                "current_segment": lead.segment,
                "timestamp": datetime.utcnow()
            }
            
        except Exception as e:
            logging.error(f"Failed to get lead analytics: {str(e)}")
            raise

    async def get_ab_test_results(self, campaign_a_id: int, campaign_b_id: int, db: Session) -> Dict[str, Any]:
        """Get results of A/B test between two campaigns"""
        try:
            # Get campaigns
            campaign_a = db.query(Campaign).filter(Campaign.id == campaign_a_id).first()
            campaign_b = db.query(Campaign).filter(Campaign.id == campaign_b_id).first()
            
            if not campaign_a or not campaign_b:
                raise ValueError("One or both campaigns not found")
                
            # Get metrics for both campaigns
            metrics_a = self._calculate_campaign_metrics(campaign_a, db)
            metrics_b = self._calculate_campaign_metrics(campaign_b, db)
            
            # Calculate statistical significance
            confidence = self._calculate_significance(
                metrics_a["conversion_rate"],
                metrics_b["conversion_rate"],
                metrics_a["unique_leads"],
                metrics_b["unique_leads"]
            )
            
            # Determine winner
            if metrics_a["conversion_rate"] > metrics_b["conversion_rate"]:
                winner = "A"
                improvement = ((metrics_a["conversion_rate"] - metrics_b["conversion_rate"]) 
                             / metrics_b["conversion_rate"] * 100)
            else:
                winner = "B"
                improvement = ((metrics_b["conversion_rate"] - metrics_a["conversion_rate"])
                             / metrics_a["conversion_rate"] * 100)
            
            return {
                "campaign_a": {
                    "id": campaign_a_id,
                    "metrics": metrics_a
                },
                "campaign_b": {
                    "id": campaign_b_id,
                    "metrics": metrics_b
                },
                "winner": winner,
                "improvement_percentage": improvement,
                "confidence_level": confidence,
                "significant": confidence > self.config["significance_threshold"],
                "timestamp": datetime.utcnow()
            }
            
        except Exception as e:
            logging.error(f"Failed to get A/B test results: {str(e)}")
            raise

    def _calculate_significance(self, rate_a: float, rate_b: float, 
                              sample_a: int, sample_b: int) -> float:
        """Calculate statistical significance between two conversion rates"""
        try:
            from scipy import stats
            
            # Calculate z-score
            p1 = rate_a
            p2 = rate_b
            n1 = sample_a
            n2 = sample_b
            
            # Pooled standard error
            se = ((p1 * (1 - p1) / n1) + (p2 * (1 - p2) / n2)) ** 0.5
            
            # Z-score
            z = (p1 - p2) / se
            
            # Convert to confidence level
            confidence = stats.norm.cdf(abs(z))
            
            return confidence
            
        except ImportError:
            logging.warning("scipy not installed, using simplified significance calculation")
            # Simplified calculation if scipy not available
            return 0.95 if abs(rate_a - rate_b) > 0.1 else 0.5 