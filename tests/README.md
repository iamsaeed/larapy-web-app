# Larapy Test Framework

A comprehensive testing framework for the MyApp Larapy application, featuring unit, feature, and integration tests.

## Test Structure

```
tests/
├── __init__.py              # Test package initialization
├── base.py                  # Base test classes
├── config.py                # Test configuration
├── conftest.py              # pytest configuration and fixtures
├── runner.py                # Test runner utility
├── unit/                    # Unit tests
│   ├── __init__.py
│   └── test_demo_unit.py    # Demo unit test
├── feature/                 # Feature tests
│   ├── __init__.py
│   └── test_demo_feature.py # Demo feature test
└── integration/             # Integration tests
    ├── __init__.py
    └── test_demo_integration.py # Demo integration test
```

## Test Types

### 1. Unit Tests (`tests/unit/`)
Test individual components in isolation:
- Test single functions, methods, or classes
- Mock external dependencies
- Fast execution
- High code coverage

### 2. Feature Tests (`tests/feature/`)
Test user-facing functionality:
- Test complete user workflows
- Test from user's perspective
- Test UI interactions and user journeys
- Validate business requirements

### 3. Integration Tests (`tests/integration/`)
Test component interactions:
- Test how components work together
- Test database interactions
- Test external service integrations
- Test middleware pipelines

## Running Tests

### Using the Test Runner

```bash
# Run all tests
python tests/runner.py

# Run specific test type
python tests/runner.py unit
python tests/runner.py feature
python tests/runner.py integration
```

### Using Python unittest

```bash
# Run all tests
python -m unittest discover tests

# Run specific test type
python -m unittest discover tests/unit
python -m unittest discover tests/feature
python -m unittest discover tests/integration

# Run specific test file
python -m unittest tests.unit.test_demo_unit
```

### Using individual test files

```bash
# Run unit tests
python tests/unit/test_demo_unit.py

# Run feature tests
python tests/feature/test_demo_feature.py

# Run integration tests
python tests/integration/test_demo_integration.py
```

## Demo Tests Included

### Unit Test Demo (`test_demo_unit.py`)
- Tests HomeController methods with mocked dependencies
- Tests utility functions (string manipulation, validation)
- Demonstrates isolated component testing

### Feature Test Demo (`test_demo_feature.py`)
- Tests welcome page user workflow
- Tests user navigation functionality
- Tests form submission workflows
- Demonstrates user-centric testing

### Integration Test Demo (`test_demo_integration.py`)
- Tests controller-service integration
- Tests middleware pipeline integration
- Tests full request-response cycle
- Demonstrates multi-component testing

## Test Configuration

The test framework uses `tests/config.py` for configuration:

- **Environment**: Set to 'testing' mode
- **Database**: Uses in-memory SQLite for fast testing
- **Logging**: Reduced verbosity during tests
- **Test Data**: Configurable fixtures and temp directories

## Base Test Classes

All tests inherit from base classes in `tests/base.py`:

- **`TestCase`**: Base class for all tests
- **`UnitTestCase`**: Specialized for unit tests
- **`FeatureTestCase`**: Specialized for feature tests
- **`IntegrationTestCase`**: Specialized for integration tests

## Best Practices

1. **Unit Tests**: Mock all external dependencies
2. **Feature Tests**: Test from user perspective
3. **Integration Tests**: Use real components when possible
4. **Naming**: Use descriptive test method names
5. **Structure**: Follow Arrange-Act-Assert pattern
6. **Isolation**: Each test should be independent

## Adding New Tests

1. Choose the appropriate test type (unit/feature/integration)
2. Create test file with `test_` prefix
3. Import appropriate base class
4. Write descriptive test methods with `test_` prefix
5. Follow Arrange-Act-Assert pattern

Example:
```python
from tests.base import UnitTestCase

class TestMyComponent(UnitTestCase):
    def test_my_method_returns_expected_value(self):
        # Arrange
        component = MyComponent()
        
        # Act
        result = component.my_method()
        
        # Assert
        self.assertEqual(result, expected_value)
```
