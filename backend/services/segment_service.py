from sqlalchemy.orm import Session
from typing import List, Dict, Any
from datetime import datetime, timedelta

from ..models.lead import Lead
from ..models.event import Event

class SegmentService:
    def __init__(self, db: Session):
        self.db = db

    def segment_by_engagement(self, days: int = 30) -> Dict[str, List[Lead]]:
        """
        Segment leads based on their engagement level in the last X days.
        Returns a dictionary with segments: highly_engaged, moderately_engaged, low_engaged
        """
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        # Get all leads with their event counts
        leads_with_events = (
            self.db.query(Lead, func.count(Event.id).label('event_count'))
            .outerjoin(Event)
            .filter(Event.timestamp >= cutoff_date)
            .group_by(Lead.id)
            .all()
        )
        
        segments = {
            'highly_engaged': [],
            'moderately_engaged': [],
            'low_engaged': []
        }
        
        for lead, event_count in leads_with_events:
            if event_count >= 10:
                segments['highly_engaged'].append(lead)
            elif event_count >= 5:
                segments['moderately_engaged'].append(lead)
            else:
                segments['low_engaged'].append(lead)
                
        return segments

    def segment_by_company_size(self) -> Dict[str, List[Lead]]:
        """
        Segment leads based on their company size.
        """
        segments = {
            'enterprise': [],
            'mid_market': [],
            'small_business': []
        }
        
        leads = self.db.query(Lead).all()
        
        for lead in leads:
            company_data = lead.data.get('company', {})
            employee_count = company_data.get('employees', 0)
            
            if employee_count >= 1000:
                segments['enterprise'].append(lead)
            elif employee_count >= 50:
                segments['mid_market'].append(lead)
            else:
                segments['small_business'].append(lead)
                
        return segments

    def segment_by_lead_score(self) -> Dict[str, List[Lead]]:
        """
        Segment leads based on their lead score.
        """
        segments = {
            'hot': [],
            'warm': [],
            'cold': []
        }
        
        leads = self.db.query(Lead).all()
        
        for lead in leads:
            if lead.lead_score >= 80:
                segments['hot'].append(lead)
            elif lead.lead_score >= 50:
                segments['warm'].append(lead)
            else:
                segments['cold'].append(lead)
                
        return segments

    def get_segment_counts(self, segment_type: str) -> Dict[str, int]:
        """
        Get the count of leads in each segment for a given segment type.
        """
        if segment_type == 'engagement':
            segments = self.segment_by_engagement()
        elif segment_type == 'company_size':
            segments = self.segment_by_company_size()
        elif segment_type == 'lead_score':
            segments = self.segment_by_lead_score()
        else:
            raise ValueError(f"Invalid segment type: {segment_type}")
            
        return {
            segment: len(leads)
            for segment, leads in segments.items()
        } 