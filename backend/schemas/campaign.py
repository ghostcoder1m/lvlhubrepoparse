from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class CampaignBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    type: str = Field(..., description="Type of campaign (email, social, etc.)")
    target_audience: Optional[str] = Field(None, max_length=200)
    budget: Optional[float] = Field(None, ge=0)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class CampaignCreate(CampaignBase):
    pass

class CampaignUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    type: Optional[str] = None
    status: Optional[str] = Field(None, description="Campaign status (draft, active, paused, completed)")
    target_audience: Optional[str] = Field(None, max_length=200)
    budget: Optional[float] = Field(None, ge=0)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class CampaignResponse(CampaignBase):
    id: int
    status: str
    created_at: datetime
    created_by: int
    last_modified_at: Optional[datetime] = None
    last_modified_by: Optional[int] = None
    launched_at: Optional[datetime] = None
    launched_by: Optional[int] = None
    leads_count: Optional[int] = Field(0, description="Number of leads in the campaign")
    conversion_rate: Optional[float] = Field(0.0, description="Campaign conversion rate")

    class Config:
        from_attributes = True
