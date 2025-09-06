#!/usr/bin/env python3
"""
Application Entry Point

This is the main entry point for the Larapy application.
Similar to Laravel's public/index.php, this file bootstraps
and runs the application.
"""

import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import the bootstrapped application
from bootstrap.app import app


def main():
    """
    Main application entry point
    """
    print("🚀 Starting Larapy Application")
    print("=" * 50)
    print("Framework: Laravel concepts in Python Flask")
    print("Architecture: Service Container + Dependency Injection")
    print("ORM: Eloquent-like models with Query Builder")
    print("Routing: Laravel-style routing with middleware")
    print("=" * 50)
    
    # Available endpoints
    print("\n📍 Available Endpoints:")
    print("GET  /                 - Welcome page")
    print("GET  /about            - About page")  
    print("GET  /health           - Health check")
    print("GET  /api/status       - API status")
    print("GET  /api/users        - List users")
    print("POST /api/users        - Create user")
    print("GET  /api/users/{id}   - Get specific user")
    print("GET  /demo/container   - Container demo")
    print("GET  /demo/orm         - ORM demo")
    print("GET  /demo/middleware  - Middleware demo")
    
    print(f"\n🌐 Server starting on http://127.0.0.1:5000")
    print("Press Ctrl+C to stop the server")
    print("=" * 50)
    
    # Run the application
    try:
        app.run(host='127.0.0.1', port=5000, debug=True)
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"\n❌ Application error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
