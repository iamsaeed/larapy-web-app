"""Factory for Category model"""

from ..factory.factory import Factory
from app.Models.Category import Category


class CategoryFactory(Factory):
    """Factory for Category model"""
    
    model = Category

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
        """Factory state for active categorys"""
        return self.state({
            'active': True,
        })

    def inactive(self):
        """Factory state for inactive categorys"""
        return self.state({
            'active': False,
        })
