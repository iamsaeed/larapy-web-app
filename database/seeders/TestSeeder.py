"""Database seeder for Test"""

from ..seeder.seeder import Seeder


class TestSeeder(Seeder):
    """Seeder for Test data"""

    def run(self):
        """Run the database seeds"""
        # Implement your seeding logic here
        # Example:
        
        # Using model factory
        # from database.factories.TestFactory import TestFactory
        # TestFactory().count(10).create()
        
        # Or direct model creation
        # from app.Models.Test import Test
        # Test.create([
        #     {'name': 'Example 1'},
        #     {'name': 'Example 2'},
        # ])
        
        pass
