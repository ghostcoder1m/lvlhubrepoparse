from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException
from datetime import datetime, timedelta
import time

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, requests_per_minute: int = 60):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.requests = {}
        
    def _clean_old_requests(self, client_id: str):
        """Remove requests older than 1 minute"""
        current_time = time.time()
        self.requests[client_id] = [
            req_time for req_time in self.requests.get(client_id, [])
            if current_time - req_time < 60
        ]
        
    async def dispatch(self, request: Request, call_next):
        client_id = request.client.host
        
        # Clean old requests
        self._clean_old_requests(client_id)
        
        # Check current usage
        current_requests = len(self.requests.get(client_id, []))
        if current_requests >= self.requests_per_minute:
            raise HTTPException(
                status_code=429,
                detail="Too many requests. Please try again later."
            )
            
        # Add current request
        if client_id not in self.requests:
            self.requests[client_id] = []
        self.requests[client_id].append(time.time())
        
        # Process request
        response = await call_next(request)
        return response 