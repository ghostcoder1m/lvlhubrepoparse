from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class SignupForm(BaseModel):
    email: EmailStr
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    company: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    source: str = Field(default="web_form")
    
    # Optional fields for additional information
    job_title: Optional[str] = Field(None, max_length=100)
    industry: Optional[str] = Field(None, max_length=100)
    company_size: Optional[str] = Field(None, max_length=50)
    interests: Optional[list[str]] = Field(default_factory=list)
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "john.doe@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "company": "Acme Inc",
                "phone": "123-456-7890",
                "job_title": "Marketing Manager",
                "industry": "Technology",
                "company_size": "50-200",
                "interests": ["marketing automation", "lead generation"]
            }
        } 