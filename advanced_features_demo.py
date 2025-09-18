"""Advanced Database Features Demo"""

# This demo showcases all the advanced features we've implemented:
# 1. Soft Deletes
# 2. Model Events and Observers  
# 3. Global Scopes
# 4. Raw Expressions
# 5. Query Scopes

print("=== Advanced Database Features Demo ===")
print()

# Soft Deletes Example
print("1. SOFT DELETES")
print("===============")
print("""
# Model with soft deletes
class User(Model, SoftDeletes):
    table = 'users'
    fillable = ['name', 'email']

# Usage:
user = User.find(1)
user.delete()  # Soft delete (sets deleted_at)
print(user.trashed())  # True

# Query with soft deletes
User.all()  # Only non-deleted records
User.with_trashed().get()  # Include soft deleted
User.only_trashed().get()  # Only soft deleted

# Restore soft deleted
user.restore()
User.restore_all([1, 2, 3])  # Restore multiple

# Permanent delete
user.force_delete()
User.force_delete_all([4, 5, 6])
""")

# Model Events Example
print("2. MODEL EVENTS & OBSERVERS")
print("===========================")
print("""
# Observer class
class UserObserver:
    def creating(self, user):
        print(f"Creating: {user.name}")
    
    def created(self, user):
        print(f"Created: {user.name}")
        # Send welcome email, etc.
    
    def updating(self, user):
        if user.is_dirty('email'):
            print("Email is changing")
    
    def deleting(self, user):
        # Can prevent deletion by returning False
        return user.can_be_deleted()

# Register observer
User.observe(UserObserver)

# Individual event listeners
@User.creating
def validate_user(user):
    if not user.email:
        raise ValueError("Email required")

@User.updated
def clear_cache(user):
    cache.forget(f"user.{user.id}")

# Events are fired automatically:
user = User.create({'name': 'John'})  # Fires creating, created
user.update({'name': 'Jane'})  # Fires updating, updated
user.delete()  # Fires deleting, deleted
""")

# Global Scopes Example
print("3. GLOBAL SCOPES")
print("================")
print("""
# Custom global scope
class ActiveScope(Scope):
    def apply(self, builder, model):
        builder.where('active', True)

# Model with global scope
class User(Model):
    def __init__(self):
        super().__init__()
        self.add_global_scope('active', ActiveScope())

# Usage:
User.all()  # Only active users (scope applied automatically)
User.with_global_scope('active', ActiveScope()).get()  # Explicit
User.without_global_scope('active').get()  # Without scope

# Soft delete scope (built-in)
class User(Model, SoftDeletes):
    pass  # SoftDeletingScope added automatically

User.all()  # Only non-deleted (scope applied)
User.with_trashed().get()  # Without soft delete scope
""")

# Raw Expressions Example  
print("4. RAW EXPRESSIONS")
print("==================")
print("""
from larapy.database.query.expressions import raw, case, exists

# Raw SQL
users = User.select(raw('COUNT(*) as total')).get()

# CASE expressions
User.select(
    'name',
    case('status')
        .when('active', 'Active User')
        .when('inactive', 'Inactive User')
        .else_('Unknown')
        .end().as_('status_label')
).get()

# EXISTS subqueries
User.where(
    exists(
        Post.select(raw('1'))
            .where_raw('posts.user_id = users.id')
    )
).get()

# Aggregates
User.select(
    raw('COUNT(*) as user_count'),
    raw('AVG(age) as avg_age'),
    raw('MAX(created_at) as latest')
).get()

# JSON operations (MySQL/PostgreSQL)
User.where(
    JsonExpression.extract('preferences', 'theme'), 
    'dark'
).get()
""")

# Query Scopes Example
print("5. QUERY SCOPES")
print("===============")
print("""
# Define scopes in model
class User(Model):
    def scope_active(self, query):
        return query.where('active', True)
    
    def scope_verified(self, query):
        return query.where_not_null('email_verified_at')
    
    def scope_with_posts(self, query):
        return query.has('posts')
    
    def scope_of_type(self, query, type_name):
        return query.where('type', type_name)

# Usage:
User.active().get()  # Active users
User.verified().get()  # Verified users
User.active().verified().get()  # Chain scopes
User.of_type('admin').get()  # Scope with parameters

# Dynamic scopes
User.where_active().get()  # Automatically calls scope_active
User.where_verified().get()  # Automatically calls scope_verified
""")

print("6. CONSOLE COMMANDS")
print("===================")
print("""
# New migration commands:
larapy migrate:status     # Show migration status
larapy migrate:install    # Create migration table  
larapy migrate:reset      # Rollback all migrations
larapy migrate:refresh    # Reset and re-run all

# Factory & Seeder commands:
larapy make:factory UserFactory --model=User
larapy make:seeder UserSeeder

# Usage in code:
# Factory
UserFactory().count(10).create()
UserFactory().active().create()

# Seeder  
class UserSeeder(Seeder):
    def run(self):
        UserFactory().count(50).create()

larapy db:seed --class=UserSeeder
""")

print()
print("=== All Advanced Features Implemented! ===")
print()
print("The Larapy database system now includes:")
print("✓ Soft Deletes with SoftDeletes concern")
print("✓ Model Events and Observers system")  
print("✓ Global Scopes for automatic query filtering")
print("✓ Raw Expressions for complex SQL")
print("✓ Query Scopes for reusable query logic")
print("✓ Additional console commands")
print("✓ Enhanced model capabilities")
print()
print("This completes the implementation of all features")
print("specified in database.md!")