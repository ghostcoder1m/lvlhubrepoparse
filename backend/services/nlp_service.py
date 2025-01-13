from typing import Dict, List, Optional, Any
import logging
from datetime import datetime
from .ai_service import AIService
from ..models.message import Message
from sqlalchemy.orm import Session
from ..config.ai_config import MODEL_PARAMETERS, FEATURE_ENGINEERING

class NLPService:
    def __init__(self):
        self.ai_service = AIService()
        self.sentiment_endpoint_id = self.ai_service.get_endpoint_id("sentiment")
        self.content_endpoint_id = self.ai_service.get_endpoint_id("content")
        self.response_endpoint_id = self.ai_service.get_endpoint_id("response")
        self.config = MODEL_PARAMETERS["nlp"]
        self.feature_config = FEATURE_ENGINEERING

    def _prepare_text_features(self, text: str) -> Dict[str, Any]:
        """Prepare text features for analysis"""
        return {
            "text": text,
            "length": len(text),
            "word_count": len(text.split()),
            "timestamp": datetime.utcnow().isoformat()
        }

    def _prepare_response_context(self, message: Message, db: Session) -> Dict[str, Any]:
        """Prepare context for response generation"""
        context = {
            "message_id": message.id,
            "lead_id": message.lead_id,
            "channel": message.channel,
            "timestamp": message.timestamp.isoformat(),
            "previous_messages": []
        }
        
        # Get recent message history
        history = db.query(Message).filter(
            Message.lead_id == message.lead_id,
            Message.id != message.id
        ).order_by(Message.timestamp.desc()).limit(
            self.config["context_window"]
        ).all()
        
        context["previous_messages"] = [
            {
                "text": msg.content,
                "timestamp": msg.timestamp.isoformat(),
                "direction": msg.direction
            }
            for msg in history
        ]
        
        return context

    async def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment of given text"""
        try:
            features = self._prepare_text_features(text)
            
            prediction = await self.ai_service.predict(
                self.sentiment_endpoint_id,
                instances=[features]
            )
            
            result = prediction[0]
            if result["confidence"] < self.config["sentiment_threshold"]:
                logging.warning(f"Low confidence sentiment prediction: {result['confidence']}")
            
            return {
                "sentiment": result["sentiment"],
                "confidence": result["confidence"],
                "scores": {
                    "positive": result["positive_score"],
                    "neutral": result["neutral_score"],
                    "negative": result["negative_score"]
                },
                "timestamp": datetime.utcnow()
            }
            
        except Exception as e:
            logging.error(f"Failed to analyze sentiment: {str(e)}")
            raise

    async def analyze_content(self, text: str) -> Dict[str, Any]:
        """Analyze content for topics, keywords, and entities"""
        try:
            features = self._prepare_text_features(text)
            
            prediction = await self.ai_service.predict(
                self.content_endpoint_id,
                instances=[features]
            )
            
            result = prediction[0]
            if result["confidence"] < self.config["content_threshold"]:
                logging.warning(f"Low confidence content analysis: {result['confidence']}")
            
            return {
                "topics": result["topics"],
                "keywords": result["keywords"],
                "entities": result["entities"],
                "categories": result["categories"],
                "confidence": result["confidence"],
                "timestamp": datetime.utcnow()
            }
            
        except Exception as e:
            logging.error(f"Failed to analyze content: {str(e)}")
            raise

    async def generate_response(self, message: Message, db: Session) -> Dict[str, Any]:
        """Generate a personalized response based on message and context"""
        try:
            # Prepare message features and context
            features = self._prepare_text_features(message.content)
            context = self._prepare_response_context(message, db)
            
            # Combine features and context
            request_data = {
                "message": features,
                "context": context
            }
            
            prediction = await self.ai_service.predict(
                self.response_endpoint_id,
                instances=[request_data]
            )
            
            result = prediction[0]
            if result["confidence"] < self.config["response_threshold"]:
                logging.warning(f"Low confidence response generation: {result['confidence']}")
            
            return {
                "response_text": result["response"],
                "confidence": result["confidence"],
                "tone": result["tone"],
                "intent": result["intent"],
                "suggested_actions": result["actions"],
                "timestamp": datetime.utcnow()
            }
            
        except Exception as e:
            logging.error(f"Failed to generate response: {str(e)}")
            raise

    async def batch_analyze_sentiment(self, texts: List[str]) -> List[Dict[str, Any]]:
        """Analyze sentiment for multiple texts in batch"""
        try:
            # Prepare features for all texts
            features = [self._prepare_text_features(text) for text in texts]
            
            # Split into batches
            batch_size = self.config["batch_size"]
            batches = [features[i:i + batch_size] for i in range(0, len(features), batch_size)]
            
            # Process each batch
            all_results = []
            for batch in batches:
                predictions = await self.ai_service.predict(
                    self.sentiment_endpoint_id,
                    instances=batch
                )
                
                for prediction in predictions:
                    if prediction["confidence"] < self.config["sentiment_threshold"]:
                        logging.warning(f"Low confidence sentiment prediction: {prediction['confidence']}")
                    
                    result = {
                        "sentiment": prediction["sentiment"],
                        "confidence": prediction["confidence"],
                        "scores": {
                            "positive": prediction["positive_score"],
                            "neutral": prediction["neutral_score"],
                            "negative": prediction["negative_score"]
                        },
                        "timestamp": datetime.utcnow()
                    }
                    all_results.append(result)
            
            return all_results
            
        except Exception as e:
            logging.error(f"Failed to batch analyze sentiment: {str(e)}")
            raise 