import os
from typing import Dict, Any

# Vertex AI Configuration
VERTEX_AI_CONFIG = {
    "project_id": os.getenv("GOOGLE_CLOUD_PROJECT_ID"),
    "location": os.getenv("VERTEX_AI_LOCATION", "us-central1"),
}

# Model Endpoint IDs
ENDPOINTS = {
    "lead_scoring": os.getenv("LEAD_SCORING_ENDPOINT_ID"),
    "content_recommendation": os.getenv("CONTENT_RECOMMENDATION_ENDPOINT_ID"),
    "campaign_recommendation": os.getenv("CAMPAIGN_RECOMMENDATION_ENDPOINT_ID"),
    "segmentation": os.getenv("SEGMENT_PREDICTION_ENDPOINT_ID"),
    "sentiment_analysis": os.getenv("SENTIMENT_ANALYSIS_ENDPOINT_ID"),
    "content_analysis": os.getenv("CONTENT_ANALYSIS_ENDPOINT_ID"),
    "response_generation": os.getenv("RESPONSE_GENERATION_ENDPOINT_ID"),
    "performance_prediction": os.getenv("PERFORMANCE_PREDICTION_ENDPOINT_ID"),
}

# Model Parameters
MODEL_PARAMETERS: Dict[str, Dict[str, Any]] = {
    "lead_scoring": {
        "threshold": 0.7,
        "batch_size": 100,
        "features": [
            "email_engagement",
            "website_visits",
            "form_submissions",
            "content_downloads",
            "social_interactions",
            "last_interaction",
            "company_size",
            "industry",
            "budget",
        ]
    },
    "recommendation": {
        "content_similarity_threshold": 0.6,
        "max_recommendations": 10,
        "personalization_weight": 0.8,
        "recency_weight": 0.2,
    },
    "segmentation": {
        "min_confidence": 0.8,
        "update_frequency": 24,  # hours
        "segment_thresholds": {
            "cold": 0.2,
            "warm": 0.4,
            "hot": 0.7,
            "champion": 0.9,
        }
    },
    "nlp": {
        "sentiment_confidence_threshold": 0.7,
        "max_keywords": 10,
        "max_topics": 5,
        "max_entities": 20,
        "response_temperature": 0.7,
        "max_response_length": 500,
    },
    "analytics": {
        "prediction_horizon": 30,  # days
        "confidence_interval": 0.95,
        "min_data_points": 100,
        "ab_test_significance": 0.05,
    }
}

# Feature Engineering Settings
FEATURE_ENGINEERING = {
    "engagement_decay_rate": 0.1,  # per day
    "interaction_weights": {
        "email_open": 1,
        "email_click": 2,
        "form_submission": 5,
        "content_download": 3,
        "website_visit": 1,
        "social_interaction": 2,
    },
    "time_windows": {
        "short_term": 7,    # days
        "medium_term": 30,  # days
        "long_term": 90,    # days
    }
}

# Monitoring and Logging
MONITORING = {
    "performance_metrics": [
        "accuracy",
        "precision",
        "recall",
        "f1_score",
        "auc_roc",
        "mean_absolute_error",
        "root_mean_squared_error",
    ],
    "log_predictions": True,
    "log_level": "INFO",
    "metric_update_frequency": 6,  # hours
}

# Error Handling
ERROR_HANDLING = {
    "max_retries": 3,
    "retry_delay": 1,  # seconds
    "fallback_threshold": 0.5,
    "cache_ttl": 3600,  # seconds
} 