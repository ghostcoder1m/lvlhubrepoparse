from fastapi import Request, status, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.exc import SQLAlchemyError
from typing import Union, Dict, Any
import traceback
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ErrorHandler(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except Exception as exc:
            return self.handle_error(exc)

    def handle_error(self, exc: Exception) -> JSONResponse:
        """Handle different types of exceptions and return appropriate responses."""
        
        if isinstance(exc, SQLAlchemyError):
            return self._handle_database_error(exc)
        elif isinstance(exc, ValueError):
            return self._handle_validation_error(exc)
        else:
            return self._handle_generic_error(exc)

    def _handle_database_error(self, exc: SQLAlchemyError) -> JSONResponse:
        """Handle database-related errors."""
        logger.error(f"Database error: {str(exc)}\n{traceback.format_exc()}")
        
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=self._create_error_response(
                "Database error occurred",
                "database_error",
                str(exc)
            )
        )

    def _handle_validation_error(self, exc: ValueError) -> JSONResponse:
        """Handle validation errors."""
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=self._create_error_response(
                "Validation error",
                "validation_error",
                str(exc)
            )
        )

    def _handle_generic_error(self, exc: Exception) -> JSONResponse:
        """Handle any other unhandled exceptions."""
        logger.error(f"Unhandled error: {str(exc)}\n{traceback.format_exc()}")
        
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=self._create_error_response(
                "An unexpected error occurred",
                "internal_server_error",
                str(exc) if not isinstance(exc, HTTPException) else exc.detail
            )
        )

    def _create_error_response(
        self,
        message: str,
        error_type: str,
        detail: Union[str, Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create a standardized error response."""
        response = {
            "success": False,
            "error": {
                "type": error_type,
                "message": message
            }
        }
        
        if detail:
            response["error"]["detail"] = detail
            
        return response 