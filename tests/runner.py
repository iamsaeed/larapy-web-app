"""
Larapy Test Runner

This module provides functionality to run all tests or specific test types.
"""

import unittest
import sys
import os
from pathlib import Path


class LarapyTestRunner:
    """Test runner for the Larapy test framework."""
    
    def __init__(self, test_dir=None):
        """Initialize the test runner."""
        if test_dir is None:
            test_dir = Path(__file__).parent
        self.test_dir = Path(test_dir)
        
        # Add test directory to Python path
        sys.path.insert(0, str(self.test_dir))
    
    def run_unit_tests(self):
        """Run all unit tests."""
        print("🧪 Running Unit Tests...")
        return self._run_tests_in_directory('unit')
    
    def run_feature_tests(self):
        """Run all feature tests."""
        print("🎭 Running Feature Tests...")
        return self._run_tests_in_directory('feature')
    
    def run_integration_tests(self):
        """Run all integration tests."""
        print("🔗 Running Integration Tests...")
        return self._run_tests_in_directory('integration')
    
    def run_all_tests(self):
        """Run all tests in sequence."""
        print("🚀 Running All Tests...\n")
        
        results = {}
        results['unit'] = self.run_unit_tests()
        print()
        results['feature'] = self.run_feature_tests()
        print()
        results['integration'] = self.run_integration_tests()
        
        self._print_summary(results)
        return results
    
    def _run_tests_in_directory(self, test_type):
        """Run tests in a specific directory."""
        test_dir = self.test_dir / test_type
        
        if not test_dir.exists():
            print(f"❌ Test directory not found: {test_dir}")
            return {'ran': 0, 'failures': 1, 'errors': 1}
        
        # Discover and run tests
        loader = unittest.TestLoader()
        suite = loader.discover(str(test_dir), pattern='test_*.py')
        
        # Create a test runner with verbosity
        runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
        result = runner.run(suite)
        
        return {
            'ran': result.testsRun,
            'failures': len(result.failures),
            'errors': len(result.errors),
            'success': len(result.failures) == 0 and len(result.errors) == 0
        }
    
    def _print_summary(self, results):
        """Print test results summary."""
        print("\n" + "="*60)
        print("📊 TEST SUMMARY")
        print("="*60)
        
        total_ran = 0
        total_failures = 0
        total_errors = 0
        
        for test_type, result in results.items():
            status = "✅ PASSED" if result.get('success', False) else "❌ FAILED"
            print(f"{test_type.upper():>12}: {status} "
                  f"(Ran: {result['ran']}, "
                  f"Failures: {result['failures']}, "
                  f"Errors: {result['errors']})")
            
            total_ran += result['ran']
            total_failures += result['failures']
            total_errors += result['errors']
        
        print("-" * 60)
        overall_status = "✅ ALL PASSED" if (total_failures == 0 and total_errors == 0) else "❌ SOME FAILED"
        print(f"{'OVERALL':>12}: {overall_status} "
              f"(Total: {total_ran}, "
              f"Failures: {total_failures}, "
              f"Errors: {total_errors})")
        print("="*60)


def main():
    """Main entry point for running tests."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Larapy Test Runner')
    parser.add_argument('test_type', nargs='?', default='all',
                       choices=['all', 'unit', 'feature', 'integration'],
                       help='Type of tests to run (default: all)')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Verbose output')
    
    args = parser.parse_args()
    
    runner = LarapyTestRunner()
    
    if args.test_type == 'unit':
        runner.run_unit_tests()
    elif args.test_type == 'feature':
        runner.run_feature_tests()
    elif args.test_type == 'integration':
        runner.run_integration_tests()
    else:
        runner.run_all_tests()


if __name__ == '__main__':
    main()
