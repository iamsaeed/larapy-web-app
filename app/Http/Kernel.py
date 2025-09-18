"""
HTTP Kernel

Defines the middleware stack for the application.
Laravel-style middleware registration and management.
"""

import sys
from pathlib import Path

# Add package path for importing Larapy security middleware
package_path = Path(__file__).parent.parent.parent / 'package-larapy'
sys.path.insert(0, str(package_path))

# Import Larapy security middleware
from larapy.http.middleware.verify_csrf_token import VerifyCSRFToken
from larapy.cookie.middleware.encrypt_cookies import EncryptCookies  
from larapy.http.middleware.handle_cors import HandleCors
from larapy.routing.middleware.throttle_requests import ThrottleRequests
from larapy.http.middleware.security_headers import SecurityHeaders, FrameGuard
from larapy.auth.middleware.authenticate import Authenticate, RedirectIfAuthenticated

# Import local config
from config.security import get_security_config


class HttpKernel:
    """
    HTTP Kernel for managing middleware stack
    """
    
    def __init__(self, app=None):
        """Initialize kernel with app instance"""
        self.app = app
        self.security_config = get_security_config()
        
        # Initialize middleware instances with configuration
        self._setup_middleware()
    
    def _setup_middleware(self):
        """Setup middleware instances with configuration"""
        
        # CSRF middleware configuration
        self.csrf_middleware = VerifyCSRFToken()
        csrf_config = self.security_config['csrf']
        self.csrf_middleware.except_routes.extend(csrf_config['exclude'])
        
        # Cookie encryption middleware
        self.encrypt_cookies = EncryptCookies()
        cookie_config = self.security_config['cookies']
        self.encrypt_cookies.except_cookies.extend(cookie_config['exclude'])
        
        # CORS middleware
        cors_config = self.security_config['cors']
        self.cors_middleware = HandleCors(cors_config)
        
        # Security headers middleware
        headers_config = self.security_config['security_headers']
        self.security_headers = SecurityHeaders(headers_config)
        
        # Frame guard middleware
        self.frame_guard = FrameGuard(headers_config['x_frame_options'])
        
        # Throttle middleware instances
        self.throttle_default = ThrottleRequests('default')
        self.throttle_api = ThrottleRequests('api')
        self.throttle_login = ThrottleRequests('login')
        
        # Authentication middleware
        self.auth_web = Authenticate(['web'])
        self.auth_api = Authenticate(['api'])
        self.guest = RedirectIfAuthenticated(['web'])
    
    @property
    def global_middleware(self):
        """
        Global middleware applied to all requests
        Laravel order: most general to most specific
        """
        return [
            self.security_headers,    # Security headers first
            self.frame_guard,         # Clickjacking protection
            self.cors_middleware,     # CORS handling
            self.encrypt_cookies,     # Cookie encryption
        ]
    
    @property 
    def web_middleware(self):
        """
        Middleware group for web routes
        """
        return [
            # self.csrf_middleware,     # CSRF protection for web forms - temporarily disabled for debugging
        ]
    
    @property
    def api_middleware(self):
        """
        Middleware group for API routes
        """
        return [
            self.throttle_api,        # API rate limiting
        ]
    
    def get_middleware_for_group(self, group):
        """
        Get middleware for a specific group
        
        Args:
            group: Middleware group name ('web', 'api', 'global')
            
        Returns:
            List of middleware instances
        """
        if group == 'global':
            return self.global_middleware
        elif group == 'web':
            return self.web_middleware  
        elif group == 'api':
            return self.api_middleware
        else:
            return []
    
    def apply_middleware_to_route(self, route_func, groups=None):
        """
        Apply middleware groups to a route function
        
        Args:
            route_func: Route function to wrap
            groups: List of middleware groups to apply
            
        Returns:
            Wrapped function with middleware applied
        """
        if groups is None:
            groups = ['global']
        
        # Collect all middleware for the groups
        middleware_stack = []
        for group in groups:
            middleware_stack.extend(self.get_middleware_for_group(group))
        
        # Apply middleware in reverse order (outermost first)
        wrapped_func = route_func
        for middleware in reversed(middleware_stack):
            wrapped_func = middleware(wrapped_func)
        
        return wrapped_func


# Create global kernel instance
kernel = None


def get_kernel(app=None):
    """Get or create the HTTP kernel instance"""
    global kernel
    if kernel is None:
        kernel = HttpKernel(app)
    return kernel


def apply_global_middleware(app, kernel_instance=None):
    """
    Apply global middleware to Flask app
    
    Args:
        app: Flask application instance
        kernel_instance: HTTP kernel instance
    """
    if kernel_instance is None:
        kernel_instance = get_kernel(app)
    
    # Apply global middleware using Flask's before/after request hooks
    @app.before_request
    def apply_security_headers():
        """Apply security headers to all responses"""
        pass
    
    @app.after_request
    def add_security_headers(response):
        """Add security headers to all responses"""
        # Apply security headers
        headers_config = kernel_instance.security_config['security_headers']
        
        if headers_config.get('x_frame_options'):
            response.headers['X-Frame-Options'] = headers_config['x_frame_options']
        
        if headers_config.get('x_content_type_options'):
            response.headers['X-Content-Type-Options'] = headers_config['x_content_type_options']
        
        if headers_config.get('x_xss_protection'):
            response.headers['X-XSS-Protection'] = headers_config['x_xss_protection']
        
        if headers_config.get('strict_transport_security'):
            response.headers['Strict-Transport-Security'] = headers_config['strict_transport_security']
        
        if headers_config.get('content_security_policy'):
            response.headers['Content-Security-Policy'] = headers_config['content_security_policy']
        
        if headers_config.get('referrer_policy'):
            response.headers['Referrer-Policy'] = headers_config['referrer_policy']
        
        if headers_config.get('permissions_policy'):
            response.headers['Permissions-Policy'] = headers_config['permissions_policy']
        
        return response
    
    return app