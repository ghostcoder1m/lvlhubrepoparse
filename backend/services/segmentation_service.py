import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
import numpy as np

from .ai_service import AIService
from ..models.lead import Lead
from ..models.user_item_interaction import UserItemInteraction
from ..config.ai_config import MODEL_PARAMETERS, FEATURE_ENGINEERING

class SegmentationService:
    def __init__(self):
        self.ai_service = AIService()
        self.endpoint_id = self.ai_service.get_endpoint_id("segmentation")
        self.config = MODEL_PARAMETERS["segmentation"]
        self.feature_config = FEATURE_ENGINEERING
        
        # Define segment mappings
        self.segment_mapping = {
            0: "Cold Prospects",
            1: "Warm Leads",
            2: "Hot Leads",
            3: "Champions",
            4: "At Risk"
        }

    def _calculate_engagement_metrics(self, interactions: List[UserItemInteraction]) -> Dict[str, float]:
        if not interactions:
            return {
                "total_interactions": 0,
                "engagement_rate": 0.0,
                "recency_score": 0.0,
                "frequency_score": 0.0,
                "conversion_rate": 0.0
            }
            
        now = datetime.utcnow()
        total = len(interactions)
        conversions = len([i for i in interactions if i.type == "conversion"])
        
        # Calculate recency score
        if interactions:
            latest = max(i.timestamp for i in interactions)
            days_since_latest = (now - latest).days
            recency_score = np.exp(-days_since_latest / self.feature_config["recency_decay"])
        else:
            recency_score = 0.0
            
        # Calculate frequency score
        frequency_window = now - timedelta(days=self.feature_config["frequency_window"])
        recent_interactions = [i for i in interactions if i.timestamp >= frequency_window]
        frequency_score = len(recent_interactions) / self.feature_config["frequency_window"]
        
        return {
            "total_interactions": total,
            "engagement_rate": total / self.feature_config["expected_interactions"] if total > 0 else 0.0,
            "recency_score": recency_score,
            "frequency_score": frequency_score,
            "conversion_rate": conversions / total if total > 0 else 0.0
        }

    def prepare_segmentation_features(self, lead: Lead, db: Session) -> Dict[str, Any]:
        features = {}
        
        # Basic lead information
        features.update({
            "lead_id": lead.id,
            "industry": lead.industry,
            "company_size": lead.company_size,
            "score": lead.score or 0.0,
            "budget": lead.budget
        })
        
        # Get interactions from the database
        interactions = db.query(UserItemInteraction).filter(
            UserItemInteraction.lead_id == lead.id
        ).all()
        
        # Calculate engagement metrics
        metrics = self._calculate_engagement_metrics(interactions)
        features.update(metrics)
        
        # Calculate interaction type distributions
        interaction_types = set(i.type for i in interactions)
        for itype in self.feature_config["interaction_types"]:
            type_count = len([i for i in interactions if i.type == itype])
            features[f"{itype}_ratio"] = type_count / len(interactions) if interactions else 0.0
        
        # Time-based features
        features["days_since_creation"] = (datetime.utcnow() - lead.created_at).days
        if lead.last_interaction:
            features["days_since_last_interaction"] = (datetime.utcnow() - lead.last_interaction).days
        else:
            features["days_since_last_interaction"] = 999  # High number for no interaction
            
        return features

    async def get_lead_segment(self, lead: Lead, db: Session) -> Dict[str, Any]:
        try:
            # Prepare features
            features = self.prepare_segmentation_features(lead, db)
            
            # Make prediction
            prediction = await self.ai_service.predict(
                self.endpoint_id,
                instances=[features]
            )
            
            # Extract segment and confidence
            segment_id = prediction[0]["segment"]
            confidence = prediction[0].get("confidence", 1.0)
            
            # Update lead if confidence meets threshold
            if confidence >= self.config["threshold"]:
                lead.segment = self.segment_mapping[segment_id]
                lead.last_segmented = datetime.utcnow()
                db.commit()
            
            return {
                "lead_id": lead.id,
                "segment": self.segment_mapping[segment_id],
                "segment_id": segment_id,
                "confidence": confidence,
                "features": features,
                "timestamp": datetime.utcnow()
            }
            
        except Exception as e:
            logging.error(f"Failed to get segment for lead {lead.id}: {str(e)}")
            raise

    async def batch_segment_leads(self, leads: List[Lead], db: Session) -> List[Dict[str, Any]]:
        try:
            # Prepare features for all leads
            all_features = []
            for lead in leads:
                features = self.prepare_segmentation_features(lead, db)
                all_features.append(features)
            
            # Split into batches
            batch_size = self.config["batch_size"]
            batches = [all_features[i:i + batch_size] for i in range(0, len(all_features), batch_size)]
            
            # Process each batch
            all_predictions = []
            for batch in batches:
                predictions = await self.ai_service.predict(
                    self.endpoint_id,
                    instances=batch
                )
                all_predictions.extend(predictions)
            
            # Update leads and prepare response
            results = []
            for lead, prediction in zip(leads, all_predictions):
                segment_id = prediction["segment"]
                confidence = prediction.get("confidence", 1.0)
                
                if confidence >= self.config["threshold"]:
                    lead.segment = self.segment_mapping[segment_id]
                    lead.last_segmented = datetime.utcnow()
                
                results.append({
                    "lead_id": lead.id,
                    "segment": self.segment_mapping[segment_id],
                    "segment_id": segment_id,
                    "confidence": confidence,
                    "timestamp": datetime.utcnow()
                })
            
            # Commit all updates
            db.commit()
            
            return results
            
        except Exception as e:
            logging.error(f"Failed to batch segment leads: {str(e)}")
            raise 