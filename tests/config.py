"""
Larapy Test Framework Configuration

This file contains configuration settings for the test framework.
"""

import os
from pathlib import Path

# Test configuration
TEST_CONFIG = {
    # Test environment settings
    'environment': 'testing',
    'debug': True,
    
    # Database settings for testing
    'database': {
        'default': 'sqlite',
        'connections': {
            'sqlite': {
                'driver': 'sqlite',
                'database': ':memory:',  # In-memory database for tests
            },
            'test_file': {
                'driver': 'sqlite',
                'database': str(Path(__file__).parent.parent / 'storage' / 'test.sqlite3'),
            }
        }
    },
    
    # Test runner settings
    'test_runner': {
        'verbosity': 2,
        'failfast': False,  # Stop on first failure
        'buffer': True,     # Buffer stdout/stderr during tests
    },
    
    # Coverage settings
    'coverage': {
        'enabled': False,   # Enable code coverage reporting
        'min_coverage': 80, # Minimum coverage percentage
    },
    
    # Test data settings
    'test_data': {
        'fixtures_dir': str(Path(__file__).parent / 'fixtures'),
        'temp_dir': str(Path(__file__).parent / 'temp'),
    },
    
    # Logging settings for tests
    'logging': {
        'level': 'WARNING',  # Only show warnings and errors during tests
        'format': '%(levelname)s: %(message)s',
    }
}

# Environment variables for testing
TEST_ENV_VARS = {
    'APP_ENV': 'testing',
    'DEBUG': 'True',
    'DATABASE_URL': 'sqlite:///:memory:',
}


def setup_test_environment():
    """Set up the test environment."""
    for key, value in TEST_ENV_VARS.items():
        os.environ[key] = value


def teardown_test_environment():
    """Clean up the test environment."""
    for key in TEST_ENV_VARS:
        if key in os.environ:
            del os.environ[key]


def get_test_config(key=None):
    """Get test configuration value."""
    if key is None:
        return TEST_CONFIG
    
    keys = key.split('.')
    value = TEST_CONFIG
    
    try:
        for k in keys:
            value = value[k]
        return value
    except (KeyError, TypeError):
        return None
