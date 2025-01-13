from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.dependencies import get_db
from app.schemas.campaign import Campaign, CampaignCreate, CampaignUpdate
from app.schemas.automation import CampaignAutomation, CampaignAutomationCreate
from app.crud import campaigns as crud
from app.crud import automation as automation_crud
from app.services import automation

router = APIRouter(prefix="/campaigns", tags=["campaigns"])

@router.get("", response_model=List[Campaign])
def get_campaigns(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all campaigns."""
    return crud.get_campaigns(db, skip=skip, limit=limit)

@router.post("", response_model=Campaign, status_code=status.HTTP_201_CREATED)
def create_campaign(campaign: CampaignCreate, db: Session = Depends(get_db)):
    """Create a new campaign."""
    return crud.create_campaign(db, campaign)

@router.get("/{campaign_id}", response_model=Campaign)
def get_campaign(campaign_id: int, db: Session = Depends(get_db)):
    """Get a specific campaign by ID."""
    db_campaign = crud.get_campaign(db, campaign_id)
    if not db_campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )
    return db_campaign

@router.patch("/{campaign_id}", response_model=Campaign)
def update_campaign(
    campaign_id: int, campaign: CampaignUpdate, db: Session = Depends(get_db)
):
    """Update a specific campaign."""
    db_campaign = crud.update_campaign(db, campaign_id, campaign)
    if not db_campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )
    return db_campaign

@router.delete("/{campaign_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_campaign(campaign_id: int, db: Session = Depends(get_db)):
    """Delete a specific campaign."""
    success = crud.delete_campaign(db, campaign_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )

@router.get("/{campaign_id}/leads")
def get_campaign_leads(campaign_id: int, db: Session = Depends(get_db)):
    """Get all leads in a campaign."""
    db_campaign = crud.get_campaign(db, campaign_id)
    if not db_campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )
    return db_campaign.leads

@router.post("/{campaign_id}/leads/{lead_id}")
def add_lead_to_campaign(
    campaign_id: int, lead_id: int, db: Session = Depends(get_db)
):
    """Add a lead to a campaign."""
    success = crud.add_lead_to_campaign(db, campaign_id, lead_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign or lead not found"
        )
    return {"status": "success", "message": "Lead added to campaign"}

@router.delete("/{campaign_id}/leads/{lead_id}")
def remove_lead_from_campaign(
    campaign_id: int, lead_id: int, db: Session = Depends(get_db)
):
    """Remove a lead from a campaign."""
    success = crud.remove_lead_from_campaign(db, campaign_id, lead_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign or lead not found"
        )
    return {"status": "success", "message": "Lead removed from campaign"}

# Campaign Automation endpoints
@router.get("/{campaign_id}/automations", response_model=List[CampaignAutomation])
def get_campaign_automations(campaign_id: int, db: Session = Depends(get_db)):
    """Get all automations for a campaign."""
    return automation_crud.get_campaign_automations(db, campaign_id)

@router.post("/{campaign_id}/automations", response_model=CampaignAutomation)
def create_campaign_automation(
    campaign_id: int,
    automation: CampaignAutomationCreate,
    db: Session = Depends(get_db)
):
    """Create a new automation for a campaign."""
    return automation_crud.create_campaign_automation(db, campaign_id, automation)

@router.patch("/{campaign_id}/automations/{automation_id}/status")
def update_automation_status(
    campaign_id: int,
    automation_id: int,
    is_active: bool,
    db: Session = Depends(get_db)
):
    """Update the status of a campaign automation."""
    db_automation = automation_crud.update_campaign_automation_status(
        db, campaign_id, automation_id, is_active
    )
    if not db_automation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign automation not found"
        )
    return db_automation

@router.delete("/{campaign_id}/automations/{automation_id}")
def delete_campaign_automation(
    campaign_id: int,
    automation_id: int,
    db: Session = Depends(get_db)
):
    """Delete a campaign automation."""
    success = automation_crud.delete_campaign_automation(
        db, campaign_id, automation_id
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign automation not found"
        )
    return {"status": "success", "message": "Campaign automation deleted"} 