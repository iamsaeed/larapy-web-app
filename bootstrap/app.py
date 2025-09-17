"""
Application Bootstrap

This file bootstraps the Larapy application with Laravel-style architecture.
Creates and configures the application instance with all necessary services.
"""

import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from larapy.foundation.application import Application
from larapy.support.facades.facade import Facade
from larapy.database.orm import DatabaseManager, Schema
from larapy.view.engine import ViewEngine
from app.Providers import AppServiceProvider


def create_application():
    """
    Create and configure the Larapy application instance
    """
    # Create application with base path
    app = Application(str(project_root))
    
    # Set up facades
    Facade.set_facade_application(app)
    
    # Set up view engine
    view_engine = ViewEngine()
    view_engine.init_app(app.flask_app, str(project_root))
    app.instance('view_engine', view_engine)
    
    # Register core service providers
    app.register(AppServiceProvider(app))
    
    # Set up database
    setup_database(app)
    
    # Load routes
    load_routes(app)
    
    return app


def setup_database(app):
    """Set up database connections and models"""
    # Create database manager
    db_manager = DatabaseManager()
    
    # Configure database connection
    db_config = {
        'driver': 'sqlite',
        'database': app.base_path('storage/app.sqlite3')
    }
    
    db_manager.add_connection('default', db_config)
    
    # Bind to container
    app.singleton('db', lambda app: db_manager)
    
    # Set up schema if needed
    connection = db_manager.connection('default')
    schema = Schema(connection)
    
    # Bind schema to container
    app.singleton('schema', lambda app: schema)
    
    # Import and set up models
    setup_models(connection)


def setup_models(connection):
    """Set up model connections"""
    # Import models and set their database connection
    try:
        from app.Models import User  # Example model
        User.set_connection(connection)
    except ImportError:
        pass  # Models not yet created


def load_routes(app):
    """Load application routes"""
    # Get router instance
    router = app.resolve('router')
    
    # Load web routes
    try:
        from routes.web import register_routes
        register_routes(router, app)
    except ImportError:
        # Set up basic route if routes not configured
        from larapy.http.response import Response
        router.get('/', lambda: Response.json({
            'message': 'Welcome to Larapy!',
            'framework': 'Laravel concepts in Python Flask',
            'status': 'Application bootstrapped successfully'
        }))


# Create the application instance
app = create_application()

if __name__ == '__main__':
    # Run the Flask application
    app.flask_app.run(debug=True, host='0.0.0.0', port=5000)
