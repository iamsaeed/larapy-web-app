"""
Timing Middleware

Measures and reports request processing time.
"""

import time
from larapy.http.middleware.middleware import Middleware
from typing import Callable


class TimingMiddleware(Middleware):
    """
    Timing Middleware
    
    Measures the time taken to process each request and adds
    timing information to the response headers.
    """
    
    def handle(self, request, next_handler: Callable):
        """
        Handle the incoming request
        
        Args:
            request: The HTTP request object
            next_handler: The next middleware/handler in the pipeline
            
        Returns:
            HTTP response with timing headers
        """
        # Record start time
        start_time = time.time()
        
        # Process the request through the pipeline
        response = next_handler(request)
        
        # Calculate processing time
        end_time = time.time()
        processing_time = end_time - start_time
        
        # Add timing information to response headers
        if hasattr(response, 'headers'):
            response.headers['X-Response-Time'] = f"{processing_time:.4f}s"
            response.headers['X-Processing-Time-Ms'] = f"{processing_time * 1000:.2f}"
        
        return response
