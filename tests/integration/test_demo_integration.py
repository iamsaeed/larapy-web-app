"""
Demo integration test for testing how components work together.

Integration tests focus on testing the interaction between multiple
components, services, and external systems.
"""

import unittest
from unittest.mock import Mock, patch
import sys
from pathlib import Path

# Add the base test class to path
sys.path.insert(0, str(Path(__file__).parent.parent))
from base import IntegrationTestCase


class TestControllerServiceIntegration(IntegrationTestCase):
    """Demo integration test for controller and service interaction."""
    
    def test_controller_with_database_service_integration(self):
        """Test that controller properly integrates with database service."""
        # Arrange - Set up integrated system
        class MockDatabaseService:
            def __init__(self):
                self.users = [
                    {'id': 1, 'name': 'John Doe', 'email': 'john@example.com'},
                    {'id': 2, 'name': 'Jane Smith', 'email': 'jane@example.com'}
                ]
            
            def find_user(self, user_id):
                for user in self.users:
                    if user['id'] == user_id:
                        return user
                return None
            
            def create_user(self, user_data):
                new_id = max([u['id'] for u in self.users]) + 1
                new_user = {'id': new_id, **user_data}
                self.users.append(new_user)
                return new_user
        
        class MockUserController:
            def __init__(self, db_service):
                self.db_service = db_service
            
            def show_user(self, user_id):
                user = self.db_service.find_user(user_id)
                if user:
                    return {
                        'status': 'success',
                        'user': user
                    }
                return {
                    'status': 'error',
                    'message': 'User not found'
                }
            
            def create_user(self, user_data):
                user = self.db_service.create_user(user_data)
                return {
                    'status': 'success',
                    'message': 'User created successfully',
                    'user': user
                }
        
        # Set up integrated system
        db_service = MockDatabaseService()
        controller = MockUserController(db_service)
        
        # Act & Assert - Test finding existing user
        result = controller.show_user(1)
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['user']['name'], 'John Doe')
        
        # Act & Assert - Test user not found
        result = controller.show_user(999)
        self.assertEqual(result['status'], 'error')
        self.assertIn('not found', result['message'])
        
        # Act & Assert - Test creating new user
        new_user_data = {'name': 'Bob Wilson', 'email': 'bob@example.com'}
        result = controller.create_user(new_user_data)
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['user']['name'], 'Bob Wilson')
        self.assertEqual(result['user']['id'], 3)
    
    def test_middleware_pipeline_integration(self):
        """Test that middleware components work together in a pipeline."""
        # Arrange - Set up middleware pipeline
        class MockRequest:
            def __init__(self, path, method='GET'):
                self.path = path
                self.method = method
                self.headers = {}
                self.metadata = {}
        
        class MockResponse:
            def __init__(self, status=200, data=None):
                self.status = status
                self.data = data or {}
                self.headers = {}
        
        class TimingMiddleware:
            def __init__(self, next_middleware=None):
                self.next = next_middleware
            
            def handle(self, request):
                import time
                start_time = time.time()
                request.metadata['start_time'] = start_time
                
                if self.next:
                    response = self.next.handle(request)
                else:
                    response = MockResponse(200, {'message': 'Success'})
                
                end_time = time.time()
                response.headers['X-Response-Time'] = f"{(end_time - start_time) * 1000:.2f}ms"
                return response
        
        class RequestIdMiddleware:
            def __init__(self, next_middleware=None):
                self.next = next_middleware
            
            def handle(self, request):
                import uuid
                request_id = str(uuid.uuid4())[:8]
                request.metadata['request_id'] = request_id
                
                if self.next:
                    response = self.next.handle(request)
                else:
                    response = MockResponse(200, {'message': 'Success'})
                
                response.headers['X-Request-ID'] = request_id
                return response
        
        class ControllerMiddleware:
            def handle(self, request):
                return MockResponse(200, {
                    'message': f'Handled {request.method} {request.path}',
                    'request_id': request.metadata.get('request_id')
                })
        
        # Set up middleware pipeline
        controller = ControllerMiddleware()
        request_id_middleware = RequestIdMiddleware(controller)
        timing_middleware = TimingMiddleware(request_id_middleware)
        
        # Act - Process request through pipeline
        request = MockRequest('/api/users', 'GET')
        response = timing_middleware.handle(request)
        
        # Assert - Verify middleware integration
        self.assertEqual(response.status, 200)
        self.assertIn('X-Request-ID', response.headers)
        self.assertIn('X-Response-Time', response.headers)
        self.assertIn('request_id', response.data)
        self.assertEqual(response.data['message'], 'Handled GET /api/users')


class TestFullStackIntegration(IntegrationTestCase):
    """Demo integration test for full stack functionality."""
    
    def test_request_response_cycle_integration(self):
        """Test complete request-response cycle integration."""
        # Arrange - Set up full stack components
        class MockDatabase:
            def __init__(self):
                self.tables = {
                    'users': [
                        {'id': 1, 'name': 'Test User', 'email': 'test@example.com'}
                    ]
                }
            
            def query(self, table, filters=None):
                if table in self.tables:
                    data = self.tables[table]
                    if filters:
                        # Simple filter implementation
                        for key, value in filters.items():
                            data = [item for item in data if item.get(key) == value]
                    return data
                return []
        
        class MockAuthService:
            def __init__(self, db):
                self.db = db
            
            def authenticate(self, email, password):
                users = self.db.query('users', {'email': email})
                if users and password == 'correct_password':
                    return users[0]
                return None
        
        class MockRouter:
            def __init__(self, auth_service):
                self.auth_service = auth_service
                self.routes = {
                    'POST /login': self.handle_login
                }
            
            def handle_request(self, method, path, data=None):
                route_key = f"{method} {path}"
                if route_key in self.routes:
                    return self.routes[route_key](data or {})
                return {'status': 404, 'message': 'Route not found'}
            
            def handle_login(self, data):
                email = data.get('email')
                password = data.get('password')
                
                if not email or not password:
                    return {
                        'status': 400,
                        'message': 'Email and password required'
                    }
                
                user = self.auth_service.authenticate(email, password)
                if user:
                    return {
                        'status': 200,
                        'message': 'Login successful',
                        'user': {'id': user['id'], 'name': user['name']}
                    }
                
                return {
                    'status': 401,
                    'message': 'Invalid credentials'
                }
        
        # Set up integrated system
        database = MockDatabase()
        auth_service = MockAuthService(database)
        router = MockRouter(auth_service)
        
        # Act & Assert - Test successful login
        login_data = {
            'email': 'test@example.com',
            'password': 'correct_password'
        }
        response = router.handle_request('POST', '/login', login_data)
        
        self.assertEqual(response['status'], 200)
        self.assertEqual(response['message'], 'Login successful')
        self.assertEqual(response['user']['name'], 'Test User')
        
        # Act & Assert - Test failed login
        wrong_login_data = {
            'email': 'test@example.com',
            'password': 'wrong_password'
        }
        response = router.handle_request('POST', '/login', wrong_login_data)
        
        self.assertEqual(response['status'], 401)
        self.assertEqual(response['message'], 'Invalid credentials')
        
        # Act & Assert - Test missing credentials
        incomplete_data = {'email': 'test@example.com'}
        response = router.handle_request('POST', '/login', incomplete_data)
        
        self.assertEqual(response['status'], 400)
        self.assertIn('required', response['message'])


if __name__ == '__main__':
    unittest.main()
