import re
from typing import Dict, Any

def clean_string(value: str) -> str:
    """Clean and standardize string values."""
    if not value:
        return value
    # Remove extra whitespace
    value = " ".join(value.split())
    # Capitalize first letter of each word for names
    return value.strip().title()

def clean_email(email: str) -> str:
    """Clean and standardize email addresses."""
    if not email:
        return email
    return email.lower().strip()

def clean_phone(phone: str) -> str:
    """Clean and standardize phone numbers."""
    if not phone:
        return phone
    # Remove all non-numeric characters
    phone = re.sub(r'\D', '', phone)
    # Format as XXX-XXX-XXXX if it's a 10-digit number
    if len(phone) == 10:
        return f"{phone[:3]}-{phone[3:6]}-{phone[6:]}"
    return phone

def clean_company_name(company: str) -> str:
    """Clean and standardize company names."""
    if not company:
        return company
    # Remove common legal suffixes
    suffixes = [' inc', ' llc', ' ltd', ' corp']
    company_lower = company.lower()
    for suffix in suffixes:
        if company_lower.endswith(suffix):
            company = company[:-len(suffix)]
    return clean_string(company)

def clean_lead_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Clean all lead data fields."""
    cleaned_data = data.copy()
    
    if 'email' in cleaned_data:
        cleaned_data['email'] = clean_email(cleaned_data['email'])
        
    if 'first_name' in cleaned_data:
        cleaned_data['first_name'] = clean_string(cleaned_data['first_name'])
        
    if 'last_name' in cleaned_data:
        cleaned_data['last_name'] = clean_string(cleaned_data['last_name'])
        
    if 'phone' in cleaned_data:
        cleaned_data['phone'] = clean_phone(cleaned_data['phone'])
        
    if 'company' in cleaned_data:
        cleaned_data['company'] = clean_company_name(cleaned_data['company'])
        
    return cleaned_data 