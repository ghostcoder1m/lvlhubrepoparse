from sqlalchemy import Column, Integer, String, DateTime
from ..database import Base

class Automation(Base):
    __tablename__ = "automations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    created_at = Column(DateTime)

    def __init__(self, name, description, created_at):
        self.name = name
        self.description = description
        self.created_at = created_at

    def __repr__(self):
        return f"<Automation(id={self.id}, name='{self.name}')>"
