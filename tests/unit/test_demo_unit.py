"""
Demo unit test for testing individual components in isolation.

Unit tests focus on testing single functions, methods, or classes
without dependencies on external systems.
"""

import unittest
from unittest.mock import Mock, patch
import sys
from pathlib import Path

# Add the base test class to path
sys.path.insert(0, str(Path(__file__).parent.parent))
from base import UnitTestCase


class TestHomeControllerUnit(UnitTestCase):
    """Demo unit test for HomeController."""
    
    def test_home_controller_index_method(self):
        """Test that HomeController.index returns correct response."""
        # Arrange - Set up test data
        expected_response = {
            'message': 'Welcome to MyApp',
            'status': 'success'
        }
        
        # Mock the HomeController
        class MockHomeController:
            def index(self):
                return {
                    'message': 'Welcome to MyApp',
                    'status': 'success'
                }
        
        controller = MockHomeController()
        
        # Act - Execute the method being tested
        result = controller.index()
        
        # Assert - Verify the results
        self.assertEqual(result['message'], expected_response['message'])
        self.assertEqual(result['status'], expected_response['status'])
        self.assertIsInstance(result, dict)
    
    def test_controller_with_mocked_dependency(self):
        """Test controller method with mocked dependencies."""
        # Arrange
        mock_service = Mock()
        mock_service.get_data.return_value = {'user_count': 42}
        
        class MockController:
            def __init__(self, service):
                self.service = service
            
            def get_stats(self):
                data = self.service.get_data()
                return {
                    'stats': data,
                    'formatted': f"Total users: {data['user_count']}"
                }
        
        controller = MockController(mock_service)
        
        # Act
        result = controller.get_stats()
        
        # Assert
        mock_service.get_data.assert_called_once()
        self.assertEqual(result['stats']['user_count'], 42)
        self.assertEqual(result['formatted'], "Total users: 42")


class TestUtilityFunctionsUnit(UnitTestCase):
    """Demo unit test for utility functions."""
    
    def test_string_helper_function(self):
        """Test a utility function for string manipulation."""
        # Arrange
        def to_snake_case(text):
            """Convert CamelCase to snake_case."""
            import re
            s1 = re.sub('([a-z0-9])([A-Z])', r'\1_\2', text)
            return s1.lower()
        
        test_cases = [
            ('CamelCase', 'camel_case'),
            ('XMLHttpRequest', 'xmlhttp_request'),
            ('SimpleTest', 'simple_test'),
            ('alreadysnake', 'alreadysnake')
        ]
        
        # Act & Assert
        for input_text, expected in test_cases:
            with self.subTest(input_text=input_text):
                result = to_snake_case(input_text)
                self.assertEqual(result, expected)
    
    def test_validation_function(self):
        """Test input validation function."""
        # Arrange
        def validate_email(email):
            """Simple email validation."""
            import re
            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            return bool(re.match(pattern, email))
        
        valid_emails = [
            'test@example.com',
            'user.name@domain.co.uk',
            'test123@test-domain.org'
        ]
        
        invalid_emails = [
            'invalid-email',
            '@domain.com',
            'test@',
            'test@.com'
        ]
        
        # Act & Assert
        for email in valid_emails:
            with self.subTest(email=email):
                self.assertTrue(validate_email(email), f"Should be valid: {email}")
        
        for email in invalid_emails:
            with self.subTest(email=email):
                self.assertFalse(validate_email(email), f"Should be invalid: {email}")


if __name__ == '__main__':
    unittest.main()
