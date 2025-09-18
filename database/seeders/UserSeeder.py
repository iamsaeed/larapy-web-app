"""User Seeder for populating users table"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'package-larapy'))

from larapy.database.seeder.seeder import Seeder
from app.Models.User import User
from database.factories.UserFactory import UserFactory


class UserSeeder(Seeder):
    """Seeder for creating sample users"""
    
    def run(self):
        """Run the seeder"""
        print("Seeding users...")
        
        # Create admin user
        admin_user = User.create({
            'name': 'Admin User',
            'email': 'admin@example.com',
            'password': 'admin123',
            'is_admin': True,
            'email_verified_at': '2024-01-01 00:00:00'
        })
        print(f"Created admin user: {admin_user.email}")
        
        # Create regular test user
        test_user = User.create({
            'name': 'Test User',
            'email': 'test@example.com',
            'password': 'test123',
            'is_admin': False,
            'email_verified_at': '2024-01-01 00:00:00'
        })
        print(f"Created test user: {test_user.email}")
        
        # Create users using factory
        try:
            factory = UserFactory()
            
            # Create 10 regular users
            users = factory.count(10).create()
            print(f"Created {len(users)} users using factory")
            
            # Create 5 verified users
            verified_users = factory.count(5).verified().create()
            print(f"Created {len(verified_users)} verified users")
            
            # Create 2 admin users
            admin_users = factory.count(2).admin().verified().create()
            print(f"Created {len(admin_users)} admin users")
            
        except Exception as e:
            print(f"Factory creation failed (expected in demo): {e}")
            # Fallback to manual creation
            for i in range(5):
                user = User.create({
                    'name': f'User {i+1}',
                    'email': f'user{i+1}@example.com',
                    'password': 'password123'
                })
                print(f"Created user: {user.email}")
        
        print("User seeding completed!")