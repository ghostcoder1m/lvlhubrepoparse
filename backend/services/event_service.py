from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional, List, Dict, Any

from ..models.event import Event
from ..models.lead import Lead

class EventService:
    def __init__(self, db: Session):
        self.db = db

    def track_event(
        self,
        event_type: str,
        properties: Dict[str, Any],
        lead_id: Optional[int] = None,
        source: str = "web"
    ) -> Event:
        """
        Track a new event with the given properties.
        """
        event = Event(
            event_type=event_type,
            lead_id=lead_id,
            source=source,
            properties=properties,
            timestamp=datetime.utcnow()
        )
        
        self.db.add(event)
        self.db.commit()
        self.db.refresh(event)
        
        return event

    def get_lead_events(
        self,
        lead_id: int,
        event_type: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Event]:
        """
        Get all events for a specific lead, optionally filtered by event type and date range.
        """
        query = self.db.query(Event).filter(Event.lead_id == lead_id)
        
        if event_type:
            query = query.filter(Event.event_type == event_type)
            
        if start_date:
            query = query.filter(Event.timestamp >= start_date)
            
        if end_date:
            query = query.filter(Event.timestamp <= end_date)
            
        return query.order_by(Event.timestamp.desc()).all()

    def get_events_by_type(
        self,
        event_type: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100
    ) -> List[Event]:
        """
        Get events of a specific type, optionally filtered by date range.
        """
        query = self.db.query(Event).filter(Event.event_type == event_type)
        
        if start_date:
            query = query.filter(Event.timestamp >= start_date)
            
        if end_date:
            query = query.filter(Event.timestamp <= end_date)
            
        return query.order_by(Event.timestamp.desc()).limit(limit).all()

    def get_lead_event_count(
        self,
        lead_id: int,
        event_type: Optional[str] = None
    ) -> int:
        """
        Get the count of events for a specific lead, optionally filtered by event type.
        """
        query = self.db.query(Event).filter(Event.lead_id == lead_id)
        
        if event_type:
            query = query.filter(Event.event_type == event_type)
            
        return query.count() 