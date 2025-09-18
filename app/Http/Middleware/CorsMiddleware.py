"""
CorsMiddleware

Cors middleware for handling HTTP requests.
"""

from larapy.http.middleware.middleware import Middleware
from typing import Callable


class CorsMiddleware(Middleware):
    """
    CorsMiddleware
    
    This middleware handles cors functionality for incoming requests.
    """
    
    def handle(self, request, next_handler: Callable):
        """
        Handle the incoming request
        
        Args:
            request: The HTTP request object
            next_handler: The next middleware/handler in the pipeline
            
        Returns:
            HTTP response
        """
        # Before processing request
        # Add your pre-processing logic here
        # Example: authentication, logging, validation
        
        # Process the request through the pipeline
        response = next_handler(request)
        
        # After processing request
        # Add your post-processing logic here
        # Example: modify response headers, logging, cleanup
        
        return response
    
    def terminate(self, request, response):
        """
        Perform any final work after the response has been sent to the browser
        
        Args:
            request: The HTTP request object
            response: The HTTP response object
        """
        # Optional: Add any cleanup or finalization logic here
        # This method is called after the response has been sent
        pass
