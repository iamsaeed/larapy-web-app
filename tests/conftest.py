"""
Test configuration and fixtures for the Larapy test framework.
"""

import pytest
import sys
import os
from pathlib import Path

# Add the app directory to Python path
app_root = Path(__file__).parent.parent
sys.path.insert(0, str(app_root))

# Add the flaravel package to Python path
package_root = app_root.parent / "package-flaravel"
sys.path.insert(0, str(package_root))


@pytest.fixture(scope="session")
def app_config():
    """Application configuration for testing."""
    return {
        'app': {
            'name': 'MyApp Test',
            'debug': True,
            'env': 'testing'
        },
        'database': {
            'default': 'sqlite',
            'connections': {
                'sqlite': {
                    'driver': 'sqlite',
                    'database': ':memory:'  # Use in-memory database for tests
                }
            }
        }
    }


@pytest.fixture(scope="session")
def test_client():
    """Test client for making HTTP requests."""
    # This would typically return a test client for your web framework
    # For now, it's a placeholder
    class MockTestClient:
        def get(self, url, **kwargs):
            return MockResponse(200, {'message': 'GET request to ' + url})
        
        def post(self, url, data=None, **kwargs):
            return MockResponse(201, {'message': 'POST request to ' + url, 'data': data})
    
    return MockTestClient()


@pytest.fixture
def mock_database():
    """Mock database connection for testing."""
    class MockDatabase:
        def __init__(self):
            self.data = {}
        
        def insert(self, table, data):
            if table not in self.data:
                self.data[table] = []
            self.data[table].append(data)
            return len(self.data[table])
        
        def select(self, table, filters=None):
            if table not in self.data:
                return []
            return self.data[table]
        
        def clear(self):
            self.data = {}
    
    db = MockDatabase()
    yield db
    db.clear()


class MockResponse:
    """Mock HTTP response for testing."""
    def __init__(self, status_code, data=None):
        self.status_code = status_code
        self.data = data or {}
    
    def json(self):
        return self.data


@pytest.fixture(autouse=True)
def setup_test_environment():
    """Setup test environment before each test."""
    # Set environment variables for testing
    os.environ['APP_ENV'] = 'testing'
    os.environ['DEBUG'] = 'True'
    
    yield
    
    # Cleanup after test
    if 'APP_ENV' in os.environ:
        del os.environ['APP_ENV']
    if 'DEBUG' in os.environ:
        del os.environ['DEBUG']
