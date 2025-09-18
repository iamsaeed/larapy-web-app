"""
PaymentServiceProvider

Service provider for payment related services and functionality.
"""

from larapy.support.service_provider import ServiceProvider
from typing import List


class PaymentServiceProvider(ServiceProvider):
    """
    PaymentServiceProvider
    
    This service provider handles the registration and bootstrapping
    of payment related services.
    """
    
    def register(self):
        """
        Register services in the container
        
        This method is called to register service bindings, singletons,
        and other services in the application's service container.
        """
        # Register your services here
        # Example:
        # self.app.bind('my_service', lambda app: MyService())
        # self.app.singleton('singleton_service', lambda app: SingletonService())
        
        pass
    
    def boot(self):
        """
        Bootstrap services
        
        This method is called after all service providers have been registered.
        Use this method to perform actions that depend on other services being available.
        """
        # Bootstrap your services here
        # Example:
        # - Configure middleware
        # - Set up event listeners
        # - Publish configuration files
        # - Register view composers
        
        pass
    
    def provides(self) -> List[str]:
        """
        Get the services provided by the provider
        
        Returns:
            List of service names that this provider offers
        """
        return [
            # List the services this provider offers
            # Example: 'my_service', 'another_service'
        ]
    
    def when(self) -> List[str]:
        """
        Get the events that trigger this service provider
        
        Returns:
            List of event names that should trigger this provider
        """
        return [
            # List events that should trigger this provider
            # Example: 'user.created', 'order.completed'
        ]
    
    def is_deferred(self) -> bool:
        """
        Determine if the provider is deferred
        
        Deferred providers are only loaded when their services are actually needed.
        
        Returns:
            True if the provider should be deferred, False otherwise
        """
        # Return True if this provider should be loaded on-demand
        # Return False if this provider should be loaded on every request
        return len(self.provides()) > 0
