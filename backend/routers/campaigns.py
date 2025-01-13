from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from ..database import get_db
from ..models.campaign import Campaign
from ..models.user import User
from ..schemas.campaign import CampaignCreate, CampaignResponse, CampaignUpdate
from ..middleware.auth import auth_handler

router = APIRouter(
    prefix="/campaigns",
    tags=["campaigns"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=CampaignResponse, status_code=status.HTTP_201_CREATED)
async def create_campaign(
    campaign: CampaignCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_handler.get_current_active_user)
):
    try:
        # Create new campaign
        db_campaign = Campaign(**campaign.dict(exclude_unset=True))
        db_campaign.created_by = current_user.id
        db_campaign.status = "draft"  # Default status
        
        db.add(db_campaign)
        db.commit()
        db.refresh(db_campaign)
        return db_campaign
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating campaign: {str(e)}"
        )

@router.get("/", response_model=List[CampaignResponse])
async def get_campaigns(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = Query(None, description="Filter by campaign status"),
    type: Optional[str] = Query(None, description="Filter by campaign type"),
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_handler.get_current_active_user)
):
    try:
        query = db.query(Campaign)
        
        # Apply filters if provided
        if status:
            query = query.filter(Campaign.status == status)
        if type:
            query = query.filter(Campaign.type == type)
            
        campaigns = query.offset(skip).limit(limit).all()
        return campaigns
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving campaigns: {str(e)}"
        )

@router.get("/{campaign_id}", response_model=CampaignResponse)
async def get_campaign(
    campaign_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_handler.get_current_active_user)
):
    try:
        campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
        if campaign is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Campaign not found"
            )
        return campaign
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving campaign: {str(e)}"
        )

@router.put("/{campaign_id}", response_model=CampaignResponse)
async def update_campaign(
    campaign_id: int,
    campaign_update: CampaignUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_handler.get_current_active_user)
):
    try:
        db_campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
        if db_campaign is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Campaign not found"
            )
        
        # Update campaign fields
        for field, value in campaign_update.dict(exclude_unset=True).items():
            setattr(db_campaign, field, value)
            
        # Update last modified timestamp and user
        db_campaign.last_modified_by = current_user.id
        
        db.commit()
        db.refresh(db_campaign)
        return db_campaign
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating campaign: {str(e)}"
        )

@router.delete("/{campaign_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_campaign(
    campaign_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_handler.get_current_active_user)
):
    try:
        db_campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
        if db_campaign is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Campaign not found"
            )
            
        # Only allow deletion of draft campaigns
        if db_campaign.status != "draft":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only draft campaigns can be deleted"
            )
            
        db.delete(db_campaign)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting campaign: {str(e)}"
        )

@router.post("/{campaign_id}/launch", response_model=CampaignResponse)
async def launch_campaign(
    campaign_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_handler.get_current_active_user)
):
    try:
        db_campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
        if db_campaign is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Campaign not found"
            )
            
        # Only draft campaigns can be launched
        if db_campaign.status != "draft":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Campaign cannot be launched from {db_campaign.status} status"
            )
            
        db_campaign.status = "active"
        db_campaign.launched_at = datetime.utcnow()
        db_campaign.launched_by = current_user.id
        
        db.commit()
        db.refresh(db_campaign)
        return db_campaign
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error launching campaign: {str(e)}"
        )
