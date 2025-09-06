"""
User Model

Represents a user in the application using the Larapy ORM.
"""

from larapy.database.orm import Model


class User(Model):
    """
    User Model
    
    Represents users in the application with Laravel-style Eloquent functionality.
    """
    
    table = 'users'
    fillable = ['name', 'email', 'password']
    guarded = ['id']
    timestamps = True
    
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
