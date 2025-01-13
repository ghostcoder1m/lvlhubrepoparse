from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship
from ..database import Base
from datetime import datetime

class UserItemInteraction(Base):
    __tablename__ = "user_item_interactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    item_id = Column(Integer)  # This could reference different types of items
    interaction_type = Column(String)  # e.g., 'viewed', 'clicked', 'purchased'
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="interactions")

    def __init__(self, user_id, item_id, interaction_type):
        self.user_id = user_id
        self.item_id = item_id
        self.interaction_type = interaction_type
