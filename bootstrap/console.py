"""
Console Bootstrap for MyApp

Bootstraps the console environment and registers the application's
console kernel, similar to Laravel's bootstrap/app.php for console.
"""

import sys
import os

# Add the package and application to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'package-larapy'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from larapy.foundation.application import Application
from app.console.kernel import ConsoleKernel


def create_console_application():
    """Create and configure the console application"""

    # Determine application base path
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Create Larapy application
    app = Application(base_path)

    # Register console kernel
    app.singleton('console.kernel', lambda app: ConsoleKernel(app))

    # Boot the application
    app.boot()

    return app


def get_console_kernel(app):
    """Get the console kernel instance"""
    return app.resolve('console.kernel')