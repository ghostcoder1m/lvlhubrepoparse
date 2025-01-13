from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional, List

from ..models.lead import Lead
from ..schemas.lead import LeadCreate, LeadUpdate
from ..utils.data_cleaning import clean_lead_data
from ..integrations.clearbit import enrich_lead_data

class LeadService:
    def __init__(self, db: Session):
        self.db = db

    def create_lead(self, lead: LeadCreate) -> Lead:
        # Clean the lead data
        cleaned_data = clean_lead_data(lead.dict())
        
        # Create lead instance
        db_lead = Lead(
            **cleaned_data,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        # Add and commit to database
        self.db.add(db_lead)
        self.db.commit()
        self.db.refresh(db_lead)
        
        # Enrich lead data asynchronously
        enriched_data = enrich_lead_data(db_lead.email)
        if enriched_data:
            db_lead.data = enriched_data
            self.db.commit()
            
        return db_lead

    def get_lead(self, lead_id: int) -> Optional[Lead]:
        return self.db.query(Lead).filter(Lead.id == lead_id).first()

    def get_leads(self, skip: int = 0, limit: int = 100) -> List[Lead]:
        return self.db.query(Lead).offset(skip).limit(limit).all()

    def update_lead(self, lead_id: int, lead_update: LeadUpdate) -> Optional[Lead]:
        db_lead = self.get_lead(lead_id)
        if not db_lead:
            return None
            
        update_data = lead_update.dict(exclude_unset=True)
        cleaned_data = clean_lead_data(update_data)
        
        for field, value in cleaned_data.items():
            setattr(db_lead, field, value)
            
        db_lead.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(db_lead)
        
        return db_lead

    def delete_lead(self, lead_id: int) -> bool:
        db_lead = self.get_lead(lead_id)
        if not db_lead:
            return False
            
        self.db.delete(db_lead)
        self.db.commit()
        return True 