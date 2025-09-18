"""Product model"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'package-larapy'))

from larapy.database.eloquent.model import Model
from datetime import datetime


class Product(Model):
    """Product model"""
    
    # Table name
    table = 'products'
    
    # Primary key
    primary_key = 'id'
    
    # Enable timestamps
    timestamps = True
    
    # Mass assignable attributes
    fillable = [
        # Add your fillable fields here
        # Example: 'name', 'email', 'description'
    ]
    
    # Hidden attributes (for serialization)
    hidden = [
        # Add hidden fields here
        # Example: 'password', 'remember_token'
    ]
    
    # Attribute casting
    casts = {
        # Add attribute casts here
        # Example: 'is_active': 'boolean', 'settings': 'json'
    }
    
    # Date attributes
    dates = [
        # Add date fields here
        # Example: 'published_at', 'deleted_at'
    ]
    
    def __init__(self, attributes=None):
        super().__init__(attributes)
    
    # Define your relationships here
    # Example:
    # def user(self):
    #     """Belongs to a user"""
    #     return self.belongs_to('User', 'user_id', 'id')
    
    # def posts(self):
    #     """Has many posts"""
    #     return self.has_many('Post', 'product_id', 'id')
    
    # Define your model methods here
    # Example:
    # def is_active(self) -> bool:
    #     """Check if the product is active"""
    #     return self.get_attribute('is_active', False)
    
    # def get_full_name(self) -> str:
    #     """Get the full name"""
    #     return f"{self.first_name} {self.last_name}"
