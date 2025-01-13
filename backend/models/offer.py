from sqlalchemy import Column, Integer, String, Float, DateTime
from ..database import Base

class Offer(Base):
    __tablename__ = "offers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    discount_percentage = Column(Float)
    start_date = Column(DateTime)
    end_date = Column(DateTime)

    def __init__(self, name, description, discount_percentage, start_date, end_date):
        self.name = name
        self.description = description
        self.discount_percentage = discount_percentage
        self.start_date = start_date
        self.end_date = end_date

    def __repr__(self):
        return f"<Offer(id={self.id}, name='{self.name}', discount_percentage={self.discount_percentage})>"
