"""
Database Integration Example

This file demonstrates how to use the Larapy database system with:
- Models and relationships
- Query Builder
- Migrations
- Factories and Seeders
- Transactions
"""

import sys
import os

# Add the package to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'package-larapy'))

# Import database components
from larapy.database import (
    configure_database, table, schema, connection, transaction,
    Model, DatabaseManager, QueryBuilder, SchemaBuilder
)

# Import models
from app.Models.User import User
from app.Models.Post import Post

def setup_database():
    """Setup database configuration"""
    print("🔧 Setting up database configuration...")
    
    # Configure the database with SQLite
    config = {
        'default': 'sqlite',
        'connections': {
            'sqlite': {
                'driver': 'sqlite',
                'database': os.path.join(os.path.dirname(__file__), 'database', 'app.sqlite'),
                'prefix': '',
                'foreign_key_constraints': True
            }
        }
    }
    
    try:
        configure_database(config)
        print("✅ Database configured successfully")
        return True
    except Exception as e:
        print(f"❌ Database configuration failed: {e}")
        return False


def demonstrate_query_builder():
    """Demonstrate Query Builder usage"""
    print("\n📊 Query Builder Examples:")
    
    try:
        # Basic table queries
        print("\n1. Basic Query Builder:")
        users_query = table('users')
        print(f"   Table query created for 'users'")
        
        # Build a complex query (won't execute without actual database)
        query = (table('users')
                .select(['id', 'name', 'email'])
                .where('status', 'active')
                .where_not_null('email_verified_at')
                .order_by('created_at', 'desc')
                .limit(10))
        
        print(f"   Complex query built with select, where, order, limit")
        
        # Join example
        posts_with_users = (table('posts')
                           .join('users', 'posts.user_id', '=', 'users.id')
                           .select(['posts.*', 'users.name as author_name'])
                           .where('posts.status', 'published'))
        
        print(f"   Join query built for posts with user data")
        
        # Aggregation examples
        user_count = table('users').count()
        print(f"   Count query created")
        
        # Subquery example
        active_users_subquery = (table('users')
                                 .select('id')
                                 .where('status', 'active'))
        
        posts_by_active_users = (table('posts')
                                .where_in('user_id', active_users_subquery))
        
        print(f"   Subquery example created")
        
        print("✅ Query Builder examples completed")
        
    except Exception as e:
        print(f"❌ Query Builder demonstration failed: {e}")


def demonstrate_schema_builder():
    """Demonstrate Schema Builder usage"""
    print("\n🏗️  Schema Builder Examples:")
    
    try:
        # Get schema builder
        schema_builder = schema()
        print("   Schema builder obtained")
        
        # Example table creation (blueprint only - won't execute)
        print("\n2. Table Creation Examples:")
        
        # Users table blueprint
        def create_users_table():
            with schema_builder.create('users') as table:
                table.id()
                table.string('name')
                table.string('email').unique()
                table.timestamp('email_verified_at').nullable()
                table.string('password')
                table.boolean('is_admin').default(False)
                table.timestamps()
        
        print("   Users table blueprint created")
        
        # Posts table blueprint
        def create_posts_table():
            with schema_builder.create('posts') as table:
                table.id()
                table.string('title')
                table.text('content')
                table.foreign_id('user_id').constrained('users')
                table.string('status').default('draft')
                table.timestamp('published_at').nullable()
                table.timestamps()
                table.index(['status', 'published_at'])
        
        print("   Posts table blueprint created")
        
        # Table modification example
        def modify_users_table():
            with schema_builder.table('users') as table:
                table.string('phone', 20).nullable()
                table.text('bio').nullable()
                table.drop_column('old_column')
        
        print("   Table modification blueprint created")
        
        print("✅ Schema Builder examples completed")
        
    except Exception as e:
        print(f"❌ Schema Builder demonstration failed: {e}")


def demonstrate_model_usage():
    """Demonstrate Eloquent Model usage"""
    print("\n🎭 Eloquent Model Examples:")
    
    try:
        print("\n3. Model Examples:")
        
        # Model instantiation
        user = User()
        user.name = "John Doe"
        user.email = "john@example.com"
        user.password = "secret123"
        print(f"   User model created: {user}")
        
        # Model with attributes
        user_with_attrs = User({
            'name': 'Jane Smith',
            'email': 'jane@example.com',
            'password': 'secret456'
        })
        print(f"   User model with attributes: {user_with_attrs}")
        
        # Demonstrate accessors
        # user.first_name = "John"
        # user.last_name = "Doe"
        # print(f"   Full name accessor: {user.full_name}")
        
        # Demonstrate mutators
        user.email = "  JOHN@EXAMPLE.COM  "  # Will be normalized
        print(f"   Email after normalization: {user.email}")
        
        # Model methods
        print(f"   User table: {user.get_table()}")
        print(f"   User key name: {user.get_key_name()}")
        print(f"   User fillable: {user.fillable}")
        
        # Create Post model
        post = Post({
            'title': 'My First Post',
            'content': 'This is the content of my first post...',
            'user_id': 1,
            'status': 'published'
        })
        print(f"   Post model created: {post}")
        
        # Demonstrate post methods
        post.title = "Updated Post Title"  # Will also update slug
        print(f"   Post after title update: {post.title}")
        
        print("✅ Model examples completed")
        
    except Exception as e:
        print(f"❌ Model demonstration failed: {e}")


def demonstrate_relationships():
    """Demonstrate Model Relationships"""
    print("\n🔗 Model Relationships Examples:")
    
    try:
        print("\n4. Relationship Examples:")
        
        # Create models
        user = User({'id': 1, 'name': 'John Doe', 'email': 'john@example.com'})
        post = Post({'id': 1, 'title': 'Sample Post', 'user_id': 1})
        
        # Relationship definitions
        print("   Relationship definitions:")
        
        # User has many posts
        user_posts = user.posts()
        print(f"   User posts relationship: {type(user_posts).__name__}")
        
        # Post belongs to user
        post_user = post.user()
        print(f"   Post user relationship: {type(post_user).__name__}")
        
        # User belongs to many roles
        user_roles = user.roles()
        print(f"   User roles relationship: {type(user_roles).__name__}")
        
        # Relationship methods (would work with actual database)
        print("\n   Relationship methods (examples):")
        print(f"   user.posts().count() - Count user's posts")
        print(f"   user.posts().where('status', 'published') - Filter posts")
        print(f"   user.roles().attach(role_id) - Attach role to user")
        print(f"   user.roles().detach(role_id) - Detach role from user")
        print(f"   post.user().first() - Get post author")
        
        print("✅ Relationship examples completed")
        
    except Exception as e:
        print(f"❌ Relationship demonstration failed: {e}")


def demonstrate_advanced_features():
    """Demonstrate Advanced Features"""
    print("\n🚀 Advanced Features Examples:")
    
    try:
        print("\n5. Advanced Examples:")
        
        # Scopes
        print("   Model Scopes:")
        print(f"   User.query().verified() - Get verified users")
        print(f"   User.query().admin() - Get admin users")
        print(f"   Post.query().published() - Get published posts")
        print(f"   Post.query().recent(30) - Get recent posts")
        
        # Mass operations
        print("\n   Mass Operations:")
        print(f"   User.create(data) - Create new user")
        print(f"   User.update_or_create(conditions, data) - Update or create")
        print(f"   User.find_or_fail(id) - Find or throw exception")
        
        # Query builder chaining
        print("\n   Query Builder Chaining:")
        print(f"   User.query().where('status', 'active').with_('posts').paginate()")
        print(f"   Post.query().published().with_('user', 'tags').recent().get()")
        
        # Eager loading
        print("\n   Eager Loading:")
        print(f"   User.query().with_('posts', 'roles').get()")
        print(f"   Post.query().with_(['user', 'comments.user']).get()")
        
        # Transactions
        print("\n   Transaction Example:")
        def create_user_with_post():
            # This would be executed in a transaction
            user = User.create({'name': 'New User', 'email': 'new@example.com'})
            post = Post.create({'title': 'First Post', 'user_id': user.id})
            return user, post
        
        print(f"   transaction(create_user_with_post) - Execute in transaction")
        
        print("✅ Advanced features examples completed")
        
    except Exception as e:
        print(f"❌ Advanced features demonstration failed: {e}")


def demonstrate_factory_and_seeding():
    """Demonstrate Factory and Seeding"""
    print("\n🏭 Factory and Seeding Examples:")
    
    try:
        print("\n6. Factory Examples:")
        
        # Import factory
        from database.factories.UserFactory import UserFactory
        
        # Create factory instance
        factory = UserFactory()
        print(f"   UserFactory created")
        
        # Factory methods (examples)
        print(f"   factory.make() - Create model instance without saving")
        print(f"   factory.create() - Create and save model instance")
        print(f"   factory.count(10).create() - Create 10 instances")
        print(f"   factory.admin().verified().create() - Create with states")
        
        # Show factory definition
        definition = factory.definition()
        print(f"   Factory definition sample: {list(definition.keys())}")
        
        print("\n   Seeding Examples:")
        print(f"   UserSeeder.run() - Run user seeder")
        print(f"   DatabaseSeeder.run() - Run all seeders")
        print(f"   seed(UserSeeder) - Run specific seeder")
        
        print("✅ Factory and seeding examples completed")
        
    except Exception as e:
        print(f"❌ Factory demonstration failed: {e}")


def demonstrate_console_commands():
    """Demonstrate Console Commands"""
    print("\n⚡ Console Commands Examples:")
    
    try:
        print("\n7. Migration Commands:")
        print(f"   python larapy migrate - Run pending migrations")
        print(f"   python larapy migrate:rollback - Rollback last migration")
        print(f"   python larapy migrate:status - Show migration status")
        print(f"   python larapy make:migration create_users_table - Create migration")
        
        print("\n   Seeding Commands:")
        print(f"   python larapy db:seed - Run database seeders")
        print(f"   python larapy db:seed --class=UserSeeder - Run specific seeder")
        
        print("\n   Other Commands:")
        print(f"   python larapy make:model User - Create model")
        print(f"   python larapy make:factory UserFactory - Create factory")
        print(f"   python larapy make:seeder UserSeeder - Create seeder")
        
        print("✅ Console commands examples completed")
        
    except Exception as e:
        print(f"❌ Console commands demonstration failed: {e}")


def main():
    """Main demonstration function"""
    print("🎉 Larapy Database System Integration Example")
    print("=" * 50)
    
    # Setup database
    if not setup_database():
        print("❌ Database setup failed. Continuing with examples...")
    
    # Run demonstrations
    demonstrate_query_builder()
    demonstrate_schema_builder()
    demonstrate_model_usage()
    demonstrate_relationships()
    demonstrate_advanced_features()
    demonstrate_factory_and_seeding()
    demonstrate_console_commands()
    
    print("\n" + "=" * 50)
    print("🎊 Integration example completed!")
    print("\nTo use this database system in your application:")
    print("1. Configure your database connection")
    print("2. Create your models inheriting from Model")
    print("3. Create migrations for your database schema")
    print("4. Use the Query Builder for complex queries")
    print("5. Create factories and seeders for test data")
    print("6. Use console commands for database operations")
    print("\nFor more examples, check the files in:")
    print("- app/Models/ - Model examples")
    print("- database/migrations/ - Migration examples")
    print("- database/factories/ - Factory examples")
    print("- database/seeders/ - Seeder examples")


if __name__ == "__main__":
    main()