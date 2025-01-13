from pydantic import BaseModel
from typing import Optional

class OfferBase(BaseModel):
    name: str
    description: Optional[str] = None
    discount_percentage: float
    start_date: str  # Use str for date representation
    end_date: str    # Use str for date representation

class OfferCreate(OfferBase):
    pass

class OfferUpdate(OfferBase):
    pass

class Offer(OfferBase):
    id: int

    class Config:
        orm_mode = True
