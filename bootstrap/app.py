"""
Application Bootstrap

This file bootstraps the Larapy application with Laravel-style architecture.
Creates and configures the application instance with all necessary services.
"""

import os
import sys
import logging
from pathlib import Path
from dotenv import load_dotenv

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Load environment variables
load_dotenv(project_root / '.env')

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
    
    # Configure Flask app with environment variables
    configure_flask_app(app)
    
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

    # Configure static file serving for build assets
    setup_static_assets(app)

    # Setup security middleware
    setup_security_middleware(app)

    return app


def configure_flask_app(app):
    """Configure Flask application with environment variables"""
    flask_app = app.flask_app
    
    # Set secret key from environment
    app_key = os.getenv('APP_KEY')
    if app_key:
        flask_app.secret_key = app_key
    else:
        # Generate a random key if not set (for development only)
        import secrets
        flask_app.secret_key = secrets.token_urlsafe(32)
        print("Warning: APP_KEY not set in .env, using generated key")
    
    # Set debug mode
    flask_app.debug = os.getenv('APP_DEBUG', 'false').lower() == 'true'
    
    # Configure session
    flask_app.config['SESSION_COOKIE_SECURE'] = os.getenv('APP_ENV') == 'production'
    flask_app.config['SESSION_COOKIE_HTTPONLY'] = True
    flask_app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    
    # Configure logging
    setup_logging(app)


def setup_logging(app):
    """Configure application logging"""
    # Create logs directory if it doesn't exist
    logs_dir = project_root / 'storage' / 'logs'
    logs_dir.mkdir(parents=True, exist_ok=True)
    
    # Configure logging
    log_file = logs_dir / 'larapy.log'
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        handlers=[
            logging.FileHandler(str(log_file)),
            logging.StreamHandler()
        ]
    )
    
    # Set Flask app logger
    app.flask_app.logger.handlers = logging.getLogger().handlers
    app.flask_app.logger.setLevel(logging.INFO)


def setup_database(app):
    """Set up database connection"""
    try:
        # Database setup would go here
        pass
    except Exception as e:
        print(f"Database setup error: {e}")


def setup_models(connection):
    """Set up model connections"""
    # Import models and set their database connection
    try:
        from app.Models import User  # Example model
        # User.set_connection(connection)  # This method may not exist yet
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
        router.get('/', lambda: {
            'message': 'Welcome to Larapy!',
            'version': '1.0.0',
            'status': 'running'
        })


def setup_static_assets(app):
    """Setup static file serving for Vite build assets"""
    from flask import send_from_directory
    import os

    build_path = os.path.join(app.base_path(), 'public', 'build')

    @app.flask_app.route('/build/<path:filename>')
    def build_assets(filename):
        """Serve Vite build assets"""
        return send_from_directory(build_path, filename)


def setup_security_middleware(app):
    """Setup security middleware for the application"""
    try:
        from app.Http.Kernel import get_kernel, apply_global_middleware
        
        # Get kernel instance
        kernel_instance = get_kernel(app)
        
        # Apply global middleware
        apply_global_middleware(app.flask_app, kernel_instance)
        
        # Store kernel in app for access in routes
        app.instance('http_kernel', kernel_instance)  # Use different key to avoid conflicts
        
        print(f"Security middleware loaded successfully. Kernel type: {type(kernel_instance)}")
        
    except ImportError as e:
        print(f"Warning: Could not load security middleware: {e}")
        # Continue without security middleware if import fails


# Create the application instance
app = create_application()

if __name__ == '__main__':
    # Run the Flask application
    app.flask_app.run(debug=True, host='0.0.0.0', port=5000)
