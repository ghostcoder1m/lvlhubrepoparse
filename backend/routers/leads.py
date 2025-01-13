from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from datetime import datetime

from ..database import get_db
from ..schemas.lead import LeadCreate, LeadUpdate, Lead
from ..services.lead_service import LeadService
from ..services.event_service import EventService
from ..services.segment_service import SegmentService

router = APIRouter()

@router.post("/leads/", response_model=Lead)
def create_lead(lead: LeadCreate, db: Session = Depends(get_db)):
    lead_service = LeadService(db)
    return lead_service.create_lead(lead)

@router.get("/leads/{lead_id}", response_model=Lead)
def get_lead(lead_id: int, db: Session = Depends(get_db)):
    lead_service = LeadService(db)
    lead = lead_service.get_lead(lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead

@router.put("/leads/{lead_id}", response_model=Lead)
def update_lead(lead_id: int, lead_update: LeadUpdate, db: Session = Depends(get_db)):
    lead_service = LeadService(db)
    lead = lead_service.update_lead(lead_id, lead_update)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead

@router.delete("/leads/{lead_id}")
def delete_lead(lead_id: int, db: Session = Depends(get_db)):
    lead_service = LeadService(db)
    if not lead_service.delete_lead(lead_id):
        raise HTTPException(status_code=404, detail="Lead not found")
    return {"message": "Lead deleted successfully"}

@router.post("/leads/{lead_id}/events")
def track_lead_event(
    lead_id: int,
    event_type: str,
    properties: Dict[str, Any],
    db: Session = Depends(get_db)
):
    # Verify lead exists
    lead_service = LeadService(db)
    lead = lead_service.get_lead(lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    # Track event
    event_service = EventService(db)
    event = event_service.track_event(
        event_type=event_type,
        properties=properties,
        lead_id=lead_id
    )
    
    return {"message": "Event tracked successfully", "event_id": event.id}

@router.get("/leads/{lead_id}/events")
def get_lead_events(
    lead_id: int,
    event_type: str = None,
    db: Session = Depends(get_db)
):
    event_service = EventService(db)
    events = event_service.get_lead_events(lead_id, event_type)
    return events

@router.get("/segments/{segment_type}")
def get_segments(segment_type: str, db: Session = Depends(get_db)):
    segment_service = SegmentService(db)
    try:
        return segment_service.get_segment_counts(segment_type)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
