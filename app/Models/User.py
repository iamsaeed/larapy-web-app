"""User model example"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'package-larapy'))

from larapy.database.eloquent.model import Model
from datetime import datetime


class User(Model):
    """User model with relationships and advanced features"""
    
    # Table name
    table = 'users'
    
    # Primary key
    primary_key = 'id'
    
    # Enable timestamps
    timestamps = True
    
    # Mass assignable attributes
    fillable = [
        'name', 'email', 'password', 'email_verified_at',
        'phone', 'address', 'city', 'state', 'zip_code'
    ]
    
    # Hidden attributes (for serialization)
    hidden = ['password', 'remember_token']
    
    # Attribute casting
    casts = {
        'email_verified_at': 'datetime',
        'is_admin': 'boolean',
        'metadata': 'json'
    }
    
    # Date attributes
    dates = ['email_verified_at', 'last_login_at']
    
    def __init__(self, attributes=None):
        super().__init__(attributes)
        
    # Relationships
    def posts(self):
        """User has many posts"""
        return self.has_many('Post', 'user_id', 'id')
    
    def profile(self):
        """User has one profile"""
        return self.has_one('UserProfile', 'user_id', 'id')
    
    def roles(self):
        """User belongs to many roles"""
        return self.belongs_to_many('Role', 'user_roles', 'user_id', 'role_id')
    
    # Accessors (getters)
    def get_full_name_attribute(self, value):
        """Get full name attribute"""
        return f"{self.first_name} {self.last_name}" if hasattr(self, 'first_name') and hasattr(self, 'last_name') else self.name
    
    def get_is_verified_attribute(self, value):
        """Check if user is verified"""
        return self.email_verified_at is not None
    
    # Mutators (setters)
    def set_password_attribute(self, value):
        """Hash password when setting"""
        import hashlib
        self.attributes['password'] = hashlib.sha256(value.encode()).hexdigest()
    
    def set_email_attribute(self, value):
        """Normalize email when setting"""
        self.attributes['email'] = value.lower().strip() if value else None
    
    # Scopes
    def scope_verified(self, query):
        """Scope for verified users"""
        return query.where_not_null('email_verified_at')
    
    def scope_admin(self, query):
        """Scope for admin users"""
        return query.where('is_admin', True)
    
    def scope_active(self, query):
        """Scope for active users"""
        return query.where('status', 'active')
    
    # Methods
    def verify_email(self):
        """Mark email as verified"""
        self.email_verified_at = datetime.now()
        self.save()
    
    def assign_role(self, role):
        """Assign a role to the user"""
        return self.roles().attach(role)
    
    def remove_role(self, role):
        """Remove a role from the user"""
        return self.roles().detach(role)
    
    def has_role(self, role_name):
        """Check if user has a specific role"""
        return self.roles().where('name', role_name).exists()
    
    def get_permissions(self):
        """Get all permissions for the user"""
        # This would typically load permissions through roles
        permissions = []
        for role in self.roles:
            permissions.extend(role.permissions)
        return list(set(permissions))
    
    @classmethod
    def create_with_profile(cls, user_data, profile_data=None):
        """Create user with profile in a transaction"""
        def create_user():
            user = cls.create(user_data)
            if profile_data:
                # user.profile().create(profile_data)
                pass
            return user
        
        from larapy.database import transaction
        return transaction(create_user)
    
    @classmethod
    def find_by_email(cls, email):
        """Find user by email"""
        return cls.query().where('email', email).first()
    
    @classmethod
    def search(cls, term):
        """Search users by name or email"""
        return cls.query().where(
            lambda q: q.where('name', 'like', f'%{term}%')
                      .or_where('email', 'like', f'%{term}%')
        )
    
    def __str__(self):
        return f"User(id={self.id}, name={self.name}, email={self.email})"
    
    @classmethod
    def find_by_email(cls, email: str):
        """
        Find a user by email address
        
        Args:
            email: The email address to search for
            
        Returns:
            User instance or None if not found
        """
        return cls.where('email', email).first()
    
    @classmethod
    def create_user(cls, name: str, email: str, password: str):
        """
        Create a new user with validation
        
        Args:
            name: User's name
            email: User's email
            password: User's password (should be hashed in real app)
            
        Returns:
            Created User instance
        """
        # In a real application, you would hash the password here
        # password = hash_password(password)
        
        return cls.create(name=name, email=email, password=password)
    
    def get_display_name(self):
        """
        Get the user's display name
        
        Returns:
            User's name or email if name is not set
        """
        return self.name if self.name else self.email
    
    def to_dict(self):
        """
        Convert user to dictionary, excluding sensitive data
        
        Returns:
            Dictionary representation of user
        """
        data = super().to_dict()
        # Remove password from output for security
        if 'password' in data:
            del data['password']
        return data
    
    def __repr__(self):
        """String representation of the user"""
        return f"<User(id={self.get_key()}, email='{self.email}')>"
