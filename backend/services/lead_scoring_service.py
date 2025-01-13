import numpy as np
from typing import Dict, Any, Optional, List
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import joblib
import json
import os
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from ..models.lead import Lead
from ..models.event import Event
from ..models.ai_model import AIModel

class LeadScoringService:
    def __init__(self, db: Session):
        self.db = db
        self.model = None
        self.scaler = None
        self._load_active_model()

    def _load_active_model(self):
        """Load the active lead scoring model from storage."""
        active_model = (
            self.db.query(AIModel)
            .filter(AIModel.name == "lead_scoring", AIModel.is_active == True)
            .first()
        )
        
        if active_model and os.path.exists(active_model.filepath):
            model_data = joblib.load(active_model.filepath)
            self.model = model_data['model']
            self.scaler = model_data['scaler']

    def _extract_features(self, lead: Lead) -> Dict[str, float]:
        """Extract features from lead data for scoring."""
        # Get events in the last 30 days
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        events = (
            self.db.query(Event)
            .filter(
                Event.lead_id == lead.id,
                Event.timestamp >= thirty_days_ago
            )
            .all()
        )

        # Calculate features
        features = {
            # Basic lead information
            'has_company': 1.0 if lead.company else 0.0,
            'has_phone': 1.0 if lead.phone else 0.0,
            
            # Event counts
            'total_events': len(events),
            'form_submissions': sum(1 for e in events if e.event_type == 'form_submitted'),
            'page_views': sum(1 for e in events if e.event_type == 'page_viewed'),
            'resource_downloads': sum(1 for e in events if e.event_type == 'resource_downloaded'),
            
            # Enriched data features
            'company_size': float(lead.data.get('company', {}).get('employees', 0)),
            'days_since_creation': (datetime.utcnow() - lead.created_at).days
        }
        
        return features

    def score_lead(self, lead: Lead) -> Optional[float]:
        """Score a lead using the active model."""
        if not self.model or not self.scaler:
            return None

        # Extract features
        features = self._extract_features(lead)
        
        # Convert to array and scale
        feature_array = np.array([list(features.values())])
        scaled_features = self.scaler.transform(feature_array)
        
        # Get prediction probability
        score = self.model.predict_proba(scaled_features)[0][1]  # Probability of positive class
        
        return float(score)

    def train_model(self, training_data: List[Dict[str, Any]]) -> Dict[str, float]:
        """Train a new lead scoring model."""
        # Prepare data
        X = []  # Features
        y = []  # Labels (converted/not converted)
        
        for data in training_data:
            features = list(self._extract_features(data['lead']).values())
            X.append(features)
            y.append(data['converted'])
            
        X = np.array(X)
        y = np.array(y)
        
        # Initialize and fit scaler
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)
        
        # Train model
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        self.model.fit(X_scaled, y)
        
        # Save model
        model_path = f"models/lead_scoring_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.joblib"
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        
        model_data = {
            'model': self.model,
            'scaler': self.scaler
        }
        joblib.dump(model_data, model_path)
        
        # Create model record
        new_model = AIModel(
            name="lead_scoring",
            version=self._get_next_version(),
            description="Lead scoring model using Random Forest",
            model_type="random_forest",
            filepath=model_path,
            is_active=True,
            parameters=json.dumps(self.model.get_params()),
            metrics=json.dumps(self._calculate_metrics(X_scaled, y))
        )
        
        # Deactivate other models
        self.db.query(AIModel).filter(
            AIModel.name == "lead_scoring",
            AIModel.is_active == True
        ).update({"is_active": False})
        
        # Save new model
        self.db.add(new_model)
        self.db.commit()
        
        return self._calculate_metrics(X_scaled, y)

    def _get_next_version(self) -> int:
        """Get the next version number for lead scoring models."""
        latest_model = (
            self.db.query(AIModel)
            .filter(AIModel.name == "lead_scoring")
            .order_by(AIModel.version.desc())
            .first()
        )
        return (latest_model.version + 1) if latest_model else 1

    def _calculate_metrics(self, X: np.ndarray, y: np.array) -> Dict[str, float]:
        """Calculate model performance metrics."""
        from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
        
        y_pred = self.model.predict(X)
        
        return {
            'accuracy': float(accuracy_score(y, y_pred)),
            'precision': float(precision_score(y, y_pred)),
            'recall': float(recall_score(y, y_pred)),
            'f1': float(f1_score(y, y_pred))
        }

    def get_feature_importance(self) -> Dict[str, float]:
        """Get feature importance scores."""
        if not self.model:
            return {}
            
        feature_names = [
            'has_company', 'has_phone', 'total_events', 'form_submissions',
            'page_views', 'resource_downloads', 'company_size', 'days_since_creation'
        ]
        
        importance_scores = self.model.feature_importances_
        return dict(zip(feature_names, importance_scores.tolist())) 