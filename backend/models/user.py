from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from ..database import Base  # Updated to relative import

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    company = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String, default="user")

    leads = relationship("Lead", back_populates="owner")
    campaigns = relationship("Campaign", back_populates="user")
    onboarding = relationship("Onboarding", back_populates="user", uselist=False)
    automations = relationship("Automation", back_populates="user")
    funnels = relationship("Funnel", back_populates="user")
    workflows = relationship("Workflow", back_populates="user")

    def __init__(self, email, hashed_password, first_name, last_name, company, is_active=True, role='user'):
        self.email = email
        self.hashed_password = hashed_password
        self.first_name = first_name
        self.last_name = last_name
        self.company = company
        self.is_active = is_active
        self.role = role

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', first_name='{self.first_name}', last_name='{self.last_name}', company='{self.company}', is_active={self.is_active}, role='{self.role}')>"
