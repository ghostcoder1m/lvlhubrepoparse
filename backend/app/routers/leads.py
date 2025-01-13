from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.dependencies import get_db
from app.schemas.lead import Lead, LeadCreate, LeadUpdate
from app.crud import leads as crud
from app.services import automation

router = APIRouter(prefix="/leads", tags=["leads"])

@router.get("", response_model=List[Lead])
def get_leads(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all leads."""
    return crud.get_leads(db, skip=skip, limit=limit)

@router.post("", response_model=Lead, status_code=status.HTTP_201_CREATED)
def create_lead(lead: LeadCreate, db: Session = Depends(get_db)):
    """Create a new lead."""
    db_lead = crud.create_lead(db, lead)
    # Trigger automation for lead creation
    automation.process_lead_created(db, db_lead)
    return db_lead

@router.get("/{lead_id}", response_model=Lead)
def get_lead(lead_id: int, db: Session = Depends(get_db)):
    """Get a specific lead by ID."""
    db_lead = crud.get_lead(db, lead_id)
    if not db_lead:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lead not found"
        )
    return db_lead

@router.patch("/{lead_id}", response_model=Lead)
def update_lead(lead_id: int, lead: LeadUpdate, db: Session = Depends(get_db)):
    """Update a specific lead."""
    db_lead = crud.get_lead(db, lead_id)
    if not db_lead:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lead not found"
        )
    
    # Get the old lead score before update
    old_score = db_lead.lead_score
    
    # Track which fields are being updated
    updated_fields = [
        field for field, value in lead.model_dump(exclude_unset=True).items()
        if getattr(db_lead, field) != value
    ]
    
    # Update the lead
    db_lead = crud.update_lead(db, lead_id, lead)
    
    # Trigger automation for lead update
    automation.process_lead_updated(db, db_lead, updated_fields)
    
    # If lead score changed, trigger score changed automation
    if "lead_score" in updated_fields:
        automation.process_score_changed(db, db_lead, old_score)
    
    return db_lead

@router.delete("/{lead_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_lead(lead_id: int, db: Session = Depends(get_db)):
    """Delete a specific lead."""
    success = crud.delete_lead(db, lead_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lead not found"
        )

@router.post("/{lead_id}/events/{event_type}")
def track_lead_event(
    lead_id: int,
    event_type: str,
    event_data: dict,
    db: Session = Depends(get_db)
):
    """Track an event for a specific lead."""
    db_lead = crud.get_lead(db, lead_id)
    if not db_lead:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lead not found"
        )
    
    # Create the event
    crud.create_lead_event(db, lead_id, event_type, event_data)
    
    # Trigger automation for event
    automation.process_event_occurred(db, db_lead, event_type, event_data)
    
    return {"status": "success", "message": "Event tracked successfully"} 