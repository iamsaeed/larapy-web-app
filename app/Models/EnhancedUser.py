"""Enhanced User model with advanced features"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../package-larapy'))

from typing import Optional, List
from larapy.database.eloquent.model import Model
from larapy.database.eloquent.concerns.soft_deletes import SoftDeletes
from larapy.database.eloquent.scopes import SoftDeletingScope


class User(Model, SoftDeletes):
    """User model with soft deletes and advanced features"""
    
    table = 'users'
    fillable = ['name', 'email', 'password', 'active']
    hidden = ['password']
    dates = ['email_verified_at']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add soft deleting scope
        self.add_global_scope('soft_deleting', SoftDeletingScope())

    # Query scopes
    def scope_active(self, query):
        """Scope for active users"""
        return query.where('active', True)
    
    def scope_verified(self, query):
        """Scope for verified users"""
        return query.where_not_null('email_verified_at')
    
    def scope_with_posts(self, query):
        """Scope for users with posts"""
        return query.has('posts')
    
    # Relationships
    def posts(self):
        """User has many posts"""
        return self.has_many('Post', 'user_id')
    
    def profile(self):
        """User has one profile"""
        return self.has_one('UserProfile', 'user_id')
    
    def roles(self):
        """User belongs to many roles"""
        return self.belongs_to_many('Role', 'user_roles', 'user_id', 'role_id')
    
    # Accessors
    def get_display_name_attribute(self):
        """Get display name (accessor)"""
        return self.attributes.get('name', 'Anonymous')
    
    def get_is_admin_attribute(self):
        """Check if user is admin"""
        return 'admin' in [role.name for role in self.roles]
    
    # Mutators
    def set_password_attribute(self, value):
        """Hash password when setting (mutator)"""
        import hashlib
        if value:
            self.attributes['password'] = hashlib.md5(value.encode()).hexdigest()
    
    def set_email_attribute(self, value):
        """Lowercase email when setting"""
        if value:
            self.attributes['email'] = value.lower()


class UserObserver:
    """Observer for User model events"""
    
    def creating(self, user):
        """Handle the User "creating" event"""
        print(f"Creating user: {user.name}")
        # You could add validation, logging, etc.
    
    def created(self, user):
        """Handle the User "created" event"""
        print(f"User created: {user.name} (ID: {user.id})")
        # Send welcome email, create profile, etc.
    
    def updating(self, user):
        """Handle the User "updating" event"""
        if user.is_dirty('email'):
            print(f"Email changing from {user.get_original('email')} to {user.email}")
    
    def updated(self, user):
        """Handle the User "updated" event"""
        print(f"User updated: {user.name}")
    
    def deleting(self, user):
        """Handle the User "deleting" event"""
        print(f"Deleting user: {user.name}")
        # You could prevent deletion under certain conditions
        # return False  # This would prevent the deletion
    
    def deleted(self, user):
        """Handle the User "deleted" event"""
        print(f"User deleted: {user.name}")
    
    def restoring(self, user):
        """Handle the User "restoring" event"""
        print(f"Restoring user: {user.name}")
    
    def restored(self, user):
        """Handle the User "restored" event"""
        print(f"User restored: {user.name}")


# Register the observer
User.observe(UserObserver)

# Register individual event listeners
@User.creating
def log_user_creation(user):
    """Log user creation"""
    print(f"About to create user: {user.email}")

@User.updated
def clear_cache_on_update(user):
    """Clear cache when user is updated"""
    print(f"Clearing cache for user: {user.id}")


if __name__ == "__main__":
    """Example usage of advanced features"""
    
    # Using query scopes
    active_users = User.active().get()
    verified_users = User.verified().get()
    active_verified_users = User.active().verified().get()
    
    # Using soft deletes
    all_users = User.all()  # Only non-deleted
    all_including_deleted = User.with_trashed().get()  # Including soft deleted
    only_deleted = User.only_trashed().get()  # Only soft deleted
    
    # Create user (will fire events)
    user = User.create({
        'name': 'John Doe',
        'email': 'JOHN@EXAMPLE.COM',  # Will be lowercased by mutator
        'password': 'secret123',  # Will be hashed by mutator
        'active': True
    })
    
    # Access computed attributes
    print(f"Display name: {user.display_name}")
    print(f"Is admin: {user.is_admin}")
    
    # Soft delete
    user.delete()  # Soft delete
    print(f"Is trashed: {user.trashed()}")
    
    # Restore
    user.restore()
    print(f"Is trashed after restore: {user.trashed()}")
    
    # Force delete (permanent)
    user.force_delete()
    
    # Restore multiple users
    User.restore_all([1, 2, 3])
    
    # Force delete multiple users
    User.force_delete_all([4, 5, 6])