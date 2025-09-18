"""User Factory for generating test data"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'package-larapy'))

from larapy.database.factory.factory import Factory
from app.Models.User import User


class UserFactory(Factory):
    """Factory for creating User model instances"""
    
    def __init__(self, **kwargs):
        super().__init__(model=User, **kwargs)
    
    def definition(self):
        """Define the model's default state"""
        return {
            'name': self.fake_name(),
            'email': self.fake_email(),
            'password': 'password123',  # This will be hashed by the model
            'phone': self.fake_phone(),
            'address': self.fake_address(),
            'city': self.fake_city(),
            'state': self.fake_state(),
            'zip_code': self.fake_zip(),
            'is_admin': False,
            'status': 'active'
        }
    
    def admin(self):
        """Create an admin user state"""
        return self.state({
            'is_admin': True,
            'name': 'Admin User'
        })
    
    def verified(self):
        """Create a verified user state"""
        return self.state({
            'email_verified_at': self.fake_past_date(30)
        })
    
    def inactive(self):
        """Create an inactive user state"""
        return self.state({
            'status': 'inactive'
        })
    
    def with_profile(self):
        """Create user with profile callback"""
        def create_profile(user):
            # This would create a user profile
            pass
        
        return self.after_creating(create_profile)


# Convenience function to create the factory
def user_factory(count=1):
    """Create UserFactory instance"""
    return UserFactory().count(count)