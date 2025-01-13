import numpy as np
from typing import List, Dict, Any, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import joblib
import json
import os
from datetime import datetime
from sqlalchemy.orm import Session

from ..models.lead import Lead
from ..models.event import Event
from ..models.ai_model import AIModel

class RecommendationService:
    def __init__(self, db: Session):
        self.db = db
        self.model = None
        self.vectorizer = None
        self._load_active_model()

    def _load_active_model(self):
        """Load the active recommendation model from storage."""
        active_model = (
            self.db.query(AIModel)
            .filter(AIModel.name == "recommendation", AIModel.is_active == True)
            .first()
        )
        
        if active_model and os.path.exists(active_model.filepath):
            model_data = joblib.load(active_model.filepath)
            self.vectorizer = model_data['vectorizer']
            self.model = model_data['similarity_matrix']

    def _create_lead_profile(self, lead: Lead) -> str:
        """Create a text profile of the lead based on their data and behavior."""
        profile_parts = []
        
        # Add basic lead information
        if lead.company:
            profile_parts.append(f"company:{lead.company}")
        if lead.data.get('company', {}).get('industry'):
            profile_parts.append(f"industry:{lead.data['company']['industry']}")
            
        # Add events
        events = (
            self.db.query(Event)
            .filter(Event.lead_id == lead.id)
            .all()
        )
        
        for event in events:
            profile_parts.append(f"event:{event.event_type}")
            if event.properties.get('interests'):
                profile_parts.extend([f"interest:{i}" for i in event.properties['interests']])
                
        return " ".join(profile_parts)

    def train_model(self, leads: List[Lead]) -> Dict[str, float]:
        """Train a new recommendation model using content-based filtering."""
        # Create lead profiles
        lead_profiles = [self._create_lead_profile(lead) for lead in leads]
        
        # Initialize and fit vectorizer
        self.vectorizer = TfidfVectorizer(
            analyzer='word',
            token_pattern=r'[^:]+:[^:\s]+',
            min_df=2
        )
        
        # Create TF-IDF matrix
        tfidf_matrix = self.vectorizer.fit_transform(lead_profiles)
        
        # Calculate similarity matrix
        self.model = cosine_similarity(tfidf_matrix)
        
        # Save model
        model_path = f"models/recommendation_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.joblib"
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        
        model_data = {
            'vectorizer': self.vectorizer,
            'similarity_matrix': self.model
        }
        joblib.dump(model_data, model_path)
        
        # Create model record
        new_model = AIModel(
            name="recommendation",
            version=self._get_next_version(),
            description="Content-based recommendation model using TF-IDF and cosine similarity",
            model_type="content_based",
            filepath=model_path,
            is_active=True,
            parameters=json.dumps({
                "vectorizer_params": self.vectorizer.get_params(),
                "n_features": len(self.vectorizer.get_feature_names_out())
            }),
            metrics=json.dumps(self._calculate_metrics())
        )
        
        # Deactivate other models
        self.db.query(AIModel).filter(
            AIModel.name == "recommendation",
            AIModel.is_active == True
        ).update({"is_active": False})
        
        # Save new model
        self.db.add(new_model)
        self.db.commit()
        
        return self._calculate_metrics()

    def get_recommendations(
        self,
        lead: Lead,
        n_recommendations: int = 5
    ) -> List[Dict[str, Any]]:
        """Get personalized recommendations for a lead."""
        if not self.model or not self.vectorizer:
            return []
            
        # Get all leads
        all_leads = self.db.query(Lead).all()
        lead_profiles = [self._create_lead_profile(l) for l in all_leads]
        
        # Get lead index
        lead_idx = next((i for i, l in enumerate(all_leads) if l.id == lead.id), None)
        if lead_idx is None:
            return []
            
        # Get similar leads
        similarities = self.model[lead_idx]
        similar_indices = np.argsort(similarities)[::-1][1:n_recommendations+1]
        
        recommendations = []
        for idx in similar_indices:
            similar_lead = all_leads[idx]
            similarity_score = similarities[idx]
            
            recommendation = {
                "lead_id": similar_lead.id,
                "similarity_score": float(similarity_score),
                "explanation": self._generate_explanation(lead, similar_lead)
            }
            recommendations.append(recommendation)
            
        return recommendations

    def _get_next_version(self) -> int:
        """Get the next version number for recommendation models."""
        latest_model = (
            self.db.query(AIModel)
            .filter(AIModel.name == "recommendation")
            .order_by(AIModel.version.desc())
            .first()
        )
        return (latest_model.version + 1) if latest_model else 1

    def _calculate_metrics(self) -> Dict[str, float]:
        """Calculate model performance metrics."""
        if not self.model or not self.vectorizer:
            return {}
            
        return {
            "n_features": len(self.vectorizer.get_feature_names_out()),
            "sparsity": float(1.0 - np.count_nonzero(self.model) / self.model.size),
            "avg_similarity": float(np.mean(self.model))
        }

    def _generate_explanation(self, lead: Lead, similar_lead: Lead) -> str:
        """Generate a human-readable explanation for the recommendation."""
        reasons = []
        
        # Compare company data
        if (lead.data.get('company', {}).get('industry') == 
            similar_lead.data.get('company', {}).get('industry')):
            reasons.append("similar industry")
            
        if abs(
            lead.data.get('company', {}).get('employees', 0) -
            similar_lead.data.get('company', {}).get('employees', 0)
        ) < 100:
            reasons.append("similar company size")
            
        # Compare interests
        lead_interests = set()
        similar_lead_interests = set()
        
        for event in self.db.query(Event).filter(Event.lead_id == lead.id).all():
            if event.properties.get('interests'):
                lead_interests.update(event.properties['interests'])
                
        for event in self.db.query(Event).filter(Event.lead_id == similar_lead.id).all():
            if event.properties.get('interests'):
                similar_lead_interests.update(event.properties['interests'])
                
        common_interests = lead_interests & similar_lead_interests
        if common_interests:
            reasons.append(f"shared interests in {', '.join(common_interests)}")
            
        if not reasons:
            return "Similar profile based on overall behavior"
            
        return "Similar profile based on " + ", ".join(reasons) 