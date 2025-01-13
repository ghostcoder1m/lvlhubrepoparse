import logging
from typing import Dict, List, Optional, Any
from google.cloud import aiplatform
from ..config.ai_config import VERTEX_AI_CONFIG, ENDPOINTS, ERROR_HANDLING
import asyncio

class AIService:
    def __init__(self):
        try:
            aiplatform.init(
                project=VERTEX_AI_CONFIG["project_id"],
                location=VERTEX_AI_CONFIG["location"]
            )
            logging.info("Successfully initialized Vertex AI")
        except Exception as e:
            logging.error(f"Failed to initialize Vertex AI: {str(e)}")
            raise

    async def predict(
        self,
        endpoint_id: str,
        instances: List[Dict[str, Any]],
        timeout: Optional[float] = None
    ) -> List[Dict[str, Any]]:
        retries = 0
        while retries < ERROR_HANDLING["max_retries"]:
            try:
                endpoint = aiplatform.Endpoint(endpoint_id)
                predictions = endpoint.predict(
                    instances=instances,
                    timeout=timeout or 120
                )
                return predictions.predictions
            except Exception as e:
                retries += 1
                if retries == ERROR_HANDLING["max_retries"]:
                    logging.error(f"Failed to get predictions after {retries} attempts: {str(e)}")
                    raise
                logging.warning(f"Prediction attempt {retries} failed: {str(e)}")
                await asyncio.sleep(ERROR_HANDLING["retry_delay"])

    async def create_dataset(
        self,
        display_name: str,
        metadata: Optional[Dict[str, Any]] = None,
        sync: bool = True
    ) -> aiplatform.Dataset:
        try:
            dataset = aiplatform.Dataset.create(
                display_name=display_name,
                metadata=metadata or {},
                sync=sync
            )
            logging.info(f"Successfully created dataset: {display_name}")
            return dataset
        except Exception as e:
            logging.error(f"Failed to create dataset: {str(e)}")
            raise

    def get_endpoint_id(self, service_type: str) -> str:
        endpoint_id = ENDPOINTS.get(service_type)
        if not endpoint_id:
            raise ValueError(f"No endpoint ID configured for service type: {service_type}")
        return endpoint_id 