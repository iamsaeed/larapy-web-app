"""
Demo feature test for testing user-facing functionality.

Feature tests focus on testing complete user workflows and interactions
from the user's perspective.
"""

import unittest
from unittest.mock import Mock, patch
import sys
from pathlib import Path

# Add the base test class to path
sys.path.insert(0, str(Path(__file__).parent.parent))
from base import FeatureTestCase


class TestWelcomePageFeature(FeatureTestCase):
    """Demo feature test for the welcome page functionality."""
    
    def test_user_can_visit_welcome_page(self):
        """Test that a user can visit the welcome page and see content."""
        # Arrange - Set up mock HTTP client
        class MockHttpClient:
            def get(self, url):
                if url == '/':
                    return MockResponse(200, {
                        'content': '<h1>Welcome to MyApp</h1>',
                        'title': 'Welcome'
                    })
                return MockResponse(404, {'error': 'Not Found'})
        
        class MockResponse:
            def __init__(self, status_code, data):
                self.status_code = status_code
                self.data = data
            
            def json(self):
                return self.data
        
        client = MockHttpClient()
        
        # Act - Simulate user visiting the welcome page
        response = client.get('/')
        
        # Assert - Verify user sees the expected content
        self.assertEqual(response.status_code, 200)
        self.assertIn('Welcome to MyApp', response.json()['content'])
        self.assertEqual(response.json()['title'], 'Welcome')
    
    def test_user_navigation_workflow(self):
        """Test complete user navigation workflow."""
        # Arrange - Mock navigation system
        class MockRouter:
            def __init__(self):
                self.routes = {
                    '/': 'home',
                    '/about': 'about',
                    '/contact': 'contact'
                }
                self.current_page = None
            
            def navigate_to(self, path):
                if path in self.routes:
                    self.current_page = self.routes[path]
                    return {'status': 'success', 'page': self.current_page}
                return {'status': 'error', 'message': 'Page not found'}
        
        router = MockRouter()
        
        # Act - Simulate user navigation workflow
        home_result = router.navigate_to('/')
        about_result = router.navigate_to('/about')
        invalid_result = router.navigate_to('/invalid')
        
        # Assert - Verify navigation works as expected
        self.assertEqual(home_result['status'], 'success')
        self.assertEqual(home_result['page'], 'home')
        
        self.assertEqual(about_result['status'], 'success')
        self.assertEqual(about_result['page'], 'about')
        
        self.assertEqual(invalid_result['status'], 'error')
        self.assertIn('not found', invalid_result['message'].lower())


class TestUserInteractionFeature(FeatureTestCase):
    """Demo feature test for user interactions."""
    
    def test_user_can_submit_contact_form(self):
        """Test that a user can submit a contact form successfully."""
        # Arrange - Set up form submission system
        class MockFormHandler:
            def __init__(self):
                self.submissions = []
            
            def submit_contact_form(self, data):
                required_fields = ['name', 'email', 'message']
                
                # Validate required fields
                for field in required_fields:
                    if field not in data or not data[field]:
                        return {
                            'status': 'error',
                            'message': f'Field {field} is required'
                        }
                
                # Simulate successful submission
                submission_id = len(self.submissions) + 1
                submission = {
                    'id': submission_id,
                    'data': data,
                    'timestamp': '2025-09-06 12:00:00'
                }
                self.submissions.append(submission)
                
                return {
                    'status': 'success',
                    'message': 'Contact form submitted successfully',
                    'submission_id': submission_id
                }
        
        form_handler = MockFormHandler()
        
        # Act - User submits valid form
        form_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'message': 'Hello, this is a test message'
        }
        
        result = form_handler.submit_contact_form(form_data)
        
        # Assert - Form submission is successful
        self.assertEqual(result['status'], 'success')
        self.assertIn('successfully', result['message'])
        self.assertEqual(result['submission_id'], 1)
        self.assertEqual(len(form_handler.submissions), 1)
    
    def test_user_form_validation_errors(self):
        """Test that form validation errors are handled properly."""
        # Arrange
        class MockFormHandler:
            def submit_contact_form(self, data):
                if not data.get('email'):
                    return {
                        'status': 'error',
                        'message': 'Field email is required'
                    }
                return {'status': 'success'}
        
        form_handler = MockFormHandler()
        
        # Act - User submits invalid form
        invalid_form_data = {
            'name': 'John Doe',
            'message': 'Test message'
            # Missing email field
        }
        
        result = form_handler.submit_contact_form(invalid_form_data)
        
        # Assert - Validation error is returned
        self.assertEqual(result['status'], 'error')
        self.assertIn('email is required', result['message'])


if __name__ == '__main__':
    unittest.main()
