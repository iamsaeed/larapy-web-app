"""
Home Controller

Handles the main page requests and basic application functionality.
"""

from larapy.http.request import Request
from larapy.http.response import Response


class HomeController:
    """
    Home Controller
    
    Handles requests to the main application pages.
    """
    
    def index(self):
        """
        Display the welcome page
        """
        return Response.json({
            'message': 'Welcome to Larapy Application!',
            'framework': 'Laravel concepts in Python Flask',
            'controller': 'HomeController@index',
            'features': [
                'Service Container',
                'Dependency Injection', 
                'Laravel-style Routing',
                'Eloquent-like ORM',
                'Middleware Pipeline',
                'Service Providers',
                'Facades'
            ]
        })
    
    def about(self):
        """
        Display the about page
        """
        return Response.json({
            'page': 'About',
            'application': 'Larapy Demo App',
            'description': 'A demonstration of Laravel concepts implemented in Python using Flask',
            'architecture': {
                'container': 'Service Container with DI',
                'routing': 'Laravel-style routes',
                'orm': 'Eloquent-like models',
                'middleware': 'HTTP middleware pipeline'
            }
        })
    
    def api_status(self):
        """
        API status endpoint
        """
        return Response.json({
            'status': 'active',
            'api_version': '1.0',
            'endpoints': {
                'GET /': 'Home page',
                'GET /about': 'About page', 
                'GET /api/status': 'API status',
                'GET /api/users': 'List users',
                'POST /api/users': 'Create user'
            }
        })
    
    def health_check(self):
        """
        Health check endpoint
        """
        try:
            # You could add database connectivity check here
            return Response.json({
                'status': 'healthy',
                'timestamp': __import__('datetime').datetime.now().isoformat(),
                'services': {
                    'database': 'connected',
                    'application': 'running'
                }
            })
        except Exception as e:
            return Response.json({
                'status': 'unhealthy',
                'error': str(e)
            }, 500)
