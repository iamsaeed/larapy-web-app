"""
Web Routes

Defines all the web routes for the application.
These routes are loaded by the RouteServiceProvider.
"""

from larapy.http.response import Response
from larapy.http.request import Request


def register_routes(router):
    """
    Register all web routes
    
    Args:
        router: The Larapy router instance
    """
    
    # Home routes
    router.get('/', 'HomeController@index')
    router.get('/about', 'HomeController@about')
    
    # API routes
    router.get('/api/status', 'HomeController@api_status')
    router.get('/health', 'HomeController@health_check')
    
    # User API routes
    register_user_routes(router)
    
    # Demo routes
    register_demo_routes(router)


def register_user_routes(router):
    """Register user-related routes"""
    
    def list_users():
        """List all users"""
        try:
            from app.Models.User import User
            users = User.all()
            return Response.json([user.to_dict() for user in users])
        except Exception as e:
            return Response.json({'error': str(e)}, 500)
    
    def create_user(request: Request):
        """Create a new user"""
        try:
            from app.Models.User import User
            
            data = request.only(['name', 'email', 'password'])
            
            # Simple validation
            if not all([data.get('name'), data.get('email'), data.get('password')]):
                return Response.json({'error': 'Name, email, and password are required'}, 400)
            
            # Check if email already exists
            existing_user = User.find_by_email(data['email'])
            if existing_user:
                return Response.json({'error': 'Email already exists'}, 409)
            
            user = User.create_user(data['name'], data['email'], data['password'])
            return Response.json(user.to_dict(), 201)
            
        except Exception as e:
            return Response.json({'error': str(e)}, 500)
    
    def get_user(id: int):
        """Get a specific user"""
        try:
            from app.Models.User import User
            
            user = User.find(id)
            if not user:
                return Response.json({'error': 'User not found'}, 404)
            
            return Response.json(user.to_dict())
            
        except Exception as e:
            return Response.json({'error': str(e)}, 500)
    
    # Register the routes
    router.get('/api/users', list_users)
    router.post('/api/users', create_user)
    router.get('/api/users/{id}', get_user)


def register_demo_routes(router):
    """Register demonstration routes"""
    
    def container_demo():
        """Demonstrate service container usage"""
        return Response.json({
            'demo': 'Service Container',
            'description': 'This route demonstrates the service container and dependency injection',
            'features': [
                'Automatic dependency resolution',
                'Singleton and transient services',
                'Service binding and resolution'
            ]
        })
    
    def orm_demo():
        """Demonstrate ORM functionality"""
        try:
            from app.Models.User import User
            
            # Get user count
            user_count = User.count()
            
            # Get recent users (if any)
            recent_users = User.query().limit(3).get()
            
            return Response.json({
                'demo': 'ORM Functionality',
                'user_count': user_count,
                'recent_users': [dict(user) for user in recent_users],
                'features': [
                    'Eloquent-like models',
                    'Query builder',
                    'Relationships',
                    'Mass assignment protection'
                ]
            })
            
        except Exception as e:
            return Response.json({
                'demo': 'ORM Functionality',
                'error': str(e),
                'user_count': 0,
                'recent_users': []
            })
    
    def middleware_demo():
        """Demonstrate middleware functionality"""
        return Response.json({
            'demo': 'Middleware Pipeline',
            'description': 'This response has been processed through the middleware pipeline',
            'middleware_applied': [
                'RequestIdMiddleware - Added X-Request-ID header',
                'TimingMiddleware - Added X-Response-Time header'
            ],
            'note': 'Check the response headers to see middleware effects'
        })
    
    # Register demo routes with middleware
    router.get('/demo/container', container_demo)
    router.get('/demo/orm', orm_demo)
    router.get('/demo/middleware', middleware_demo, middleware=['request_id', 'timing'])
