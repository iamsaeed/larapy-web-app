"""
Home Controller - Handles main application pages with view rendering
"""

from larapy import Response
from flask import render_template
from app.Models.User import User
import json

class HomeController:
    """Main controller for homepage and basic routes"""
    
    def index(self):
        """Homepage with modern UI"""
        return render_template('index.html', 
            title='Welcome to Larapy',
            message='Laravel concepts in Python Flask'
        )
    
    def about(self):
        """About page with framework details"""
        return render_template('about.html',
            title='About Larapy Framework',
            features=[
                'Service Container with Dependency Injection',
                'Eloquent-like ORM with Query Builder',
                'Laravel-style Routing with Middleware',
                'Service Providers and Facades',
                'Configuration Management',
                'Jinja2 Templating Engine'
            ]
        )
    
    def contact(self):
        """Contact page with interactive form"""
        return render_template('contact.html',
            title='Contact Us'
        )
    
    def health(self):
        """Health check endpoint"""
        from flask import request
        return Response({
            'status': 'healthy',
            'framework': 'Larapy',
            'version': '1.0.0',
            'timestamp': getattr(request, 'timestamp', None),
            'uptime': 'OK'
        })
    
    def api_status(self):
        """API status endpoint"""
        return Response({
            'api': 'active',
            'framework': 'Larapy v1.0.0',
            'endpoints': {
                'users': '/api/users',
                'health': '/health',
                'status': '/api/status'
            },
            'features': [
                'Service Container',
                'ORM',
                'Middleware',
                'Routing'
            ]
        })
    
    def api_users(self):
        """List all users via API"""
        try:
            users = User.all()
            return Response({
                'success': True,
                'data': users,
                'count': len(users),
                'message': 'Users retrieved successfully'
            })
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e),
                'message': 'Failed to retrieve users'
            }, status=500)
    
    def api_user_show(self, user_id):
        """Show specific user"""
        try:
            user = User.find(user_id)
            if user:
                return Response({
                    'success': True,
                    'data': user,
                    'message': f'User {user_id} retrieved successfully'
                })
            else:
                return Response({
                    'success': False,
                    'message': f'User {user_id} not found'
                }, status=404)
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e),
                'message': 'Failed to retrieve user'
            }, status=500)
    
    def api_user_store(self):
        """Create new user"""
        from flask import request
        try:
            data = request.get_json() or {}
            name = data.get('name')
            email = data.get('email')
            
            if not name or not email:
                return Response({
                    'success': False,
                    'message': 'Name and email are required'
                }, status=400)
            
            user = User.create({
                'name': name,
                'email': email
            })
            
            return Response({
                'success': True,
                'data': user,
                'message': 'User created successfully'
            }, status=201)
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e),
                'message': 'Failed to create user'
            }, status=500)
    
    def demo_container(self):
        """Service container demo"""
        from bootstrap.app import app
        
        # Test container resolution
        resolved_services = []
        try:
            container = app.resolve('Container')
            resolved_services.append('Container')
            
            application = app.resolve('app')
            resolved_services.append('Application')
            
            flask_app = app.resolve('flask_app')
            resolved_services.append('Flask')
            
        except Exception as e:
            pass
        
        return Response({
            'message': 'Service Container is working!',
            'resolved_services': resolved_services,
            'container_info': {
                'bindings': len(app._bindings) if hasattr(app, '_bindings') else 0,
                'instances': len(app._instances) if hasattr(app, '_instances') else 0
            }
        })
    
    def demo_orm(self):
        """ORM demo"""
        try:
            users = User.all()
            user_count = len(users)
            
            return Response({
                'message': 'ORM is working!',
                'model': 'User',
                'records': user_count,
                'sample_data': users[:2] if users else [],
                'features': [
                    'Active Record Pattern',
                    'Query Builder',
                    'Relationships',
                    'Mass Assignment'
                ]
            })
        except Exception as e:
            return Response({
                'message': 'ORM Demo',
                'error': str(e),
                'note': 'Database might not be configured'
            })
    
    def demo_middleware(self):
        """Middleware demo"""
        from flask import request
        middleware_info = {
            'request_id': getattr(request, 'id', None),
            'processing_time': getattr(request, 'processing_time', None),
            'middleware_stack': [
                'RequestIdMiddleware',
                'TimingMiddleware'
            ]
        }
        
        return Response({
            'message': 'Middleware pipeline is working!',
            'request_info': middleware_info,
            'headers': dict(request.headers) if hasattr(request, 'headers') else {}
        })
    
    def test_extensions(self):
        """Test Jinja2 extensions (auth, guest, csrf, etc.)"""
        from flask import session
        
        # Set some test errors for demonstration
        session['errors'] = {
            'email': 'Email is required',
            'password': 'Password must be at least 8 characters'
        }
        
        return render_template('test_extensions.html',
            title='Jinja2 Extensions Test'
        )
