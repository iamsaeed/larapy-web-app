"""Factory for Test model"""

from ..factory.factory import Factory
from app.Models.Test import Test


class TestFactory(Factory):
    """Factory for Test model"""
    
    model = Test

    def definition(self) -> dict:
        """Define the model's default state"""
        return {
            # Define factory attributes here
            # Example:
            # 'name': self.faker.name(),
            # 'email': self.faker.unique().email(),
            # 'created_at': self.faker.date_time(),
        }

    def configure(self):
        """Configure the model factory"""
        return self

    # Define factory states
    def active(self):
        """Factory state for active tests"""
        return self.state({
            'active': True,
        })

    def inactive(self):
        """Factory state for inactive tests"""
        return self.state({
            'active': False,
        })
