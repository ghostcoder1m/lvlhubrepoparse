from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Dict, Any, Optional
import re
import html
import json
from email_validator import validate_email, EmailNotValidError

class ValidationMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        self.phone_pattern = re.compile(r'^\+?1?\d{9,15}$')
        self.url_pattern = re.compile(
            r'^https?:\/\/'
            r'(?:www\.)?'
            r'[-a-zA-Z0-9@:%._\+~#=]{1,256}'
            r'\.[a-zA-Z0-9()]{1,6}'
            r'\b(?:[-a-zA-Z0-9()@:%_\+.~#?&\/=]*)$'
        )

    async def dispatch(self, request: Request, call_next):
        """ASGI middleware implementation."""
        # Only validate POST, PUT, and PATCH requests
        if request.method.upper() in ["POST", "PUT", "PATCH"]:
            try:
                body = await request.json()
                validated_data = self.validate_request_data(body)
                # Replace request._json with validated data
                setattr(request, "_json", validated_data)
            except json.JSONDecodeError:
                raise HTTPException(status_code=400, detail="Invalid JSON format")
            except ValueError as e:
                raise HTTPException(status_code=400, detail=str(e))

        response = await call_next(request)
        return response

    def validate_request_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and sanitize request data."""
        if not isinstance(data, dict):
            raise ValueError("Request body must be a JSON object")

        validated_data = {}
        for key, value in data.items():
            # Validate and sanitize based on field name and type
            if isinstance(value, str):
                validated_data[key] = self._validate_string_field(key, value)
            elif isinstance(value, dict):
                validated_data[key] = self.validate_request_data(value)
            elif isinstance(value, list):
                validated_data[key] = [
                    self.validate_request_data(item) if isinstance(item, dict)
                    else self._validate_string_field(key, item) if isinstance(item, str)
                    else item
                    for item in value
                ]
            else:
                validated_data[key] = value

        return validated_data

    def _validate_string_field(self, field_name: str, value: str) -> str:
        """Validate and sanitize string fields based on field name."""
        # Sanitize HTML content
        value = html.escape(value.strip())

        # Validate based on field name
        lower_field = field_name.lower()
        
        if "email" in lower_field:
            return self._validate_email(value)
        elif "phone" in lower_field:
            return self._validate_phone(value)
        elif "url" in lower_field or "website" in lower_field:
            return self._validate_url(value)
        elif "password" in lower_field:
            return self._validate_password(value)
        
        return value

    def _validate_email(self, email: str) -> str:
        """Validate email format."""
        try:
            validated = validate_email(email)
            return validated.email
        except EmailNotValidError:
            raise ValueError(f"Invalid email format: {email}")

    def _validate_phone(self, phone: str) -> str:
        """Validate phone number format."""
        if not self.phone_pattern.match(phone):
            raise ValueError(f"Invalid phone number format: {phone}")
        return phone

    def _validate_url(self, url: str) -> str:
        """Validate URL format."""
        if not self.url_pattern.match(url):
            raise ValueError(f"Invalid URL format: {url}")
        return url

    def _validate_password(self, password: str) -> str:
        """Validate password strength."""
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not re.search(r"[A-Z]", password):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", password):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"\d", password):
            raise ValueError("Password must contain at least one number")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise ValueError("Password must contain at least one special character")
        return password 