from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any

from ..database import get_db
from ..forms.signup import SignupForm
from ..services.lead_service import LeadService
from ..services.event_service import EventService
from ..schemas.lead import LeadCreate

router = APIRouter()

@router.post("/forms/signup")
def handle_signup_form(
    form_data: SignupForm,
    db: Session = Depends(get_db)
):
    # Create lead from form data
    lead_data = LeadCreate(
        email=form_data.email,
        first_name=form_data.first_name,
        last_name=form_data.last_name,
        company=form_data.company,
        phone=form_data.phone,
        source=form_data.source
    )
    
    # Initialize services
    lead_service = LeadService(db)
    event_service = EventService(db)
    
    try:
        # Create lead
        lead = lead_service.create_lead(lead_data)
        
        # Track form submission event
        event_properties = {
            "form_type": "signup",
            "job_title": form_data.job_title,
            "industry": form_data.industry,
            "company_size": form_data.company_size,
            "interests": form_data.interests
        }
        
        event_service.track_event(
            event_type="form_submitted",
            properties=event_properties,
            lead_id=lead.id,
            source="web_form"
        )
        
        return {
            "message": "Form submitted successfully",
            "lead_id": lead.id
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing form submission: {str(e)}"
        ) 