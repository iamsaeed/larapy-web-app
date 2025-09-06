"""
Application Service Providers

This file contains the main service providers for the application.
Service providers are responsible for bootstrapping and registering services.
"""

from larapy.support.service_provider import ServiceProvider
from larapy.database.orm import Schema


class AppServiceProvider(ServiceProvider):
    """
    Main Application Service Provider
    
    Handles the registration and bootstrapping of core application services.
    """
    
    def register(self):
        """Register application services in the container"""
        
        # Register controllers
        self._register_controllers()
        
        # Register custom services
        self._register_custom_services()
        
        # Register middleware
        self._register_middleware()
    
    def boot(self):
        """Bootstrap application services"""
        
        # Set up database tables
        self._setup_database_tables()
        
        # Configure middleware
        self._configure_middleware()
    
    def _register_controllers(self):
        """Register application controllers"""
        from app.Http.Controllers.HomeController import HomeController
        
        self.app.bind('HomeController', lambda app: HomeController())
    
    def _register_custom_services(self):
        """Register custom application services"""
        
        # Example: Register a custom service
        # self.app.singleton('my_service', lambda app: MyService())
        pass
    
    def _register_middleware(self):
        """Register application middleware"""
        router = self.app.resolve('router')
        
        # Register middleware classes
        from app.Http.Middleware.RequestId import RequestIdMiddleware
        from app.Http.Middleware.Timing import TimingMiddleware
        
        router.middleware('request_id', 'app.Http.Middleware.RequestId.RequestIdMiddleware')
        router.middleware('timing', 'app.Http.Middleware.Timing.TimingMiddleware')
        
        # Create middleware groups
        router.middleware_group('web', ['request_id', 'timing'])
    
    def _setup_database_tables(self):
        """Set up database tables if they don't exist"""
        try:
            schema = self.app.resolve('schema')
            
            # Create users table if it doesn't exist
            if not schema.has_table('users'):
                def create_users_table(table):
                    table.id()
                    table.string('name')
                    table.string('email')
                    table.string('password')
                    table.timestamps()
                
                schema.create_table('users', create_users_table)
            
            # Create other tables as needed
            # self._create_additional_tables(schema)
            
        except Exception as e:
            print(f"Database setup error: {e}")
    
    def _configure_middleware(self):
        """Configure middleware settings"""
        # Configure middleware-specific settings
        pass
