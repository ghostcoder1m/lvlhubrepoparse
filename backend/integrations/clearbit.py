import os
import requests
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

CLEARBIT_API_KEY = os.getenv("CLEARBIT_API_KEY")
CLEARBIT_API_URL = "https://person.clearbit.com/v2/combined/find"

def enrich_lead_data(email: str) -> Optional[Dict[str, Any]]:
    """
    Enrich lead data using Clearbit's API.
    Returns enriched data if successful, None otherwise.
    """
    if not CLEARBIT_API_KEY:
        logger.warning("Clearbit API key not configured")
        return None

    try:
        headers = {
            "Authorization": f"Bearer {CLEARBIT_API_KEY}",
            "Content-Type": "application/json"
        }
        
        params = {
            "email": email
        }
        
        response = requests.get(
            CLEARBIT_API_URL,
            headers=headers,
            params=params
        )
        
        if response.status_code == 200:
            data = response.json()
            
            # Extract relevant information
            enriched_data = {
                "employment": data.get("person", {}).get("employment", {}),
                "location": data.get("person", {}).get("location", {}),
                "social": data.get("person", {}).get("social", {}),
                "company": data.get("company", {})
            }
            
            return enriched_data
            
        elif response.status_code == 404:
            logger.info(f"No enrichment data found for email: {email}")
            return None
            
        else:
            logger.error(f"Clearbit API error: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        logger.error(f"Error enriching lead data: {str(e)}")
        return None 