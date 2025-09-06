"""
Base test classes for the Larapy test framework.
"""

import unittest
from unittest.mock import Mock, patch
import sys
from pathlib import Path

# Add app to path
app_root = Path(__file__).parent.parent
sys.path.insert(0, str(app_root))


class TestCase(unittest.TestCase):
    """Base test case for all tests."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.app_config = {
            'app': {
                'name': 'MyApp Test',
                'debug': True,
                'env': 'testing'
            }
        }
    
    def tearDown(self):
        """Clean up after each test method."""
        pass


class UnitTestCase(TestCase):
    """Base class for unit tests."""
    
    def setUp(self):
        """Set up unit test fixtures."""
        super().setUp()
        # Unit tests should test individual components in isolation
        self.mock_dependencies = True


class FeatureTestCase(TestCase):
    """Base class for feature tests."""
    
    def setUp(self):
        """Set up feature test fixtures."""
        super().setUp()
        # Feature tests test user-facing functionality
        self.test_user = {
            'id': 1,
            'name': 'Test User',
            'email': 'test@example.com'
        }


class IntegrationTestCase(TestCase):
    """Base class for integration tests."""
    
    def setUp(self):
        """Set up integration test fixtures."""
        super().setUp()
        # Integration tests test how components work together
        self.database_url = 'sqlite:///:memory:'
        self.setup_test_database()
    
    def setup_test_database(self):
        """Set up test database for integration tests."""
        # This would typically set up a real test database
        self.mock_db = {
            'users': [],
            'posts': []
        }
    
    def tearDown(self):
        """Clean up integration test fixtures."""
        super().tearDown()
        # Clean up test database
        if hasattr(self, 'mock_db'):
            self.mock_db.clear()
