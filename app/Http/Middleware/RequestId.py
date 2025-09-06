"""
Request ID Middleware

Adds a unique request ID to each HTTP request for tracking and debugging.
"""

import uuid
from larapy.http.middleware.middleware import Middleware
from typing import Callable


class RequestIdMiddleware(Middleware):
    """
    Request ID Middleware
    
    Generates and adds a unique request ID to each request.
    The request ID is added to response headers for tracking.
    """
    
    def handle(self, request, next_handler: Callable):
        """
        Handle the incoming request
        
        Args:
            request: The HTTP request object
            next_handler: The next middleware/handler in the pipeline
            
        Returns:
            HTTP response with request ID header
        """
        # Generate a unique request ID
        request_id = str(uuid.uuid4())
        
        # Add request ID to request (you might want to store this in request context)
        if hasattr(request, '_request_id'):
            request._request_id = request_id
        
        # Process the request through the pipeline
        response = next_handler(request)
        
        # Add request ID to response headers
        if hasattr(response, 'headers'):
            response.headers['X-Request-ID'] = request_id
            response.headers['X-Powered-By'] = 'Larapy Framework'
        
        return response
