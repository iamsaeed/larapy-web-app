# Larapy MyApp - MySQL Configuration

This application has been configured to use MySQL as the database backend.

## Prerequisites

1. **MySQL Server**: Ensure MySQL server is installed and running
2. **Python Dependencies**: Install required packages

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `PyMySQL>=1.0.2` - MySQL connector for Python
- `cryptography>=3.4.8` - Required for MySQL authentication
- Other application dependencies

### 2. Configure Environment

The `.env` file has been configured for MySQL:

```env
# Database Configuration - MySQL
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=larapy_myapp
DB_USERNAME=root
DB_PASSWORD=
```

**Update the credentials** as needed for your MySQL setup.

### 3. Create Database

Run the setup script to create the MySQL database:

```bash
python3 setup_mysql.py
```

This script will:
- Connect to MySQL server
- Create the database if it doesn't exist
- Test the connection
- Show available databases

### 4. Run Migrations

Once the database is created, set up the tables:

```bash
# Install migration table
./larapy migrate:install

# Run migrations
./larapy migrate

# Check migration status
./larapy migrate:status
```

### 5. Seed Database (Optional)

Populate the database with sample data:

```bash
./larapy db:seed
```

## Database Configuration Details

The application uses the following MySQL configuration:

```python
'mysql': {
    'driver': 'mysql',
    'host': os.getenv('DB_HOST', '127.0.0.1'),
    'port': int(os.getenv('DB_PORT', '3306')),
    'database': os.getenv('DB_DATABASE', 'larapy_myapp'),
    'username': os.getenv('DB_USERNAME', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_unicode_ci',
    'prefix': '',
    'strict': True,
    'engine': None,
}
```

## Available Commands

```bash
# Database commands
./larapy migrate                 # Run migrations
./larapy migrate:status          # Show migration status
./larapy migrate:rollback        # Rollback last migration
./larapy migrate:reset           # Reset all migrations
./larapy migrate:refresh         # Reset and re-run all migrations

# Code generation
./larapy make:migration CreateTableName
./larapy make:factory ModelFactory
./larapy make:seeder ModelSeeder

# Database seeding
./larapy db:seed
```

## Troubleshooting

### Connection Issues

1. **MySQL not running**: Start MySQL service
   ```bash
   # Ubuntu/Debian
   sudo systemctl start mysql
   
   # macOS with Homebrew
   brew services start mysql
   ```

2. **Access denied**: Check username/password in `.env`

3. **Database doesn't exist**: Run `python3 setup_mysql.py`

4. **Permission denied**: Ensure MySQL user has CREATE DATABASE privileges

### Dependencies Issues

1. **PyMySQL not found**: Install with `pip install PyMySQL cryptography`

2. **Import errors**: Ensure virtual environment is activated

## Example Usage

```python
from app.Models.User import User
from app.Models.Post import Post

# Create user
user = User.create({
    'name': 'John Doe',
    'email': 'john@example.com'
})

# Create post
post = Post.create({
    'title': 'My First Post',
    'content': 'This is the content...',
    'user_id': user.id
})

# Query with relationships
user_with_posts = User.with_('posts').find(1)
print(f"User {user_with_posts.name} has {len(user_with_posts.posts)} posts")
```

## Migration to MySQL Complete ✅

The application has been successfully configured to use MySQL with:
- ✅ Updated environment configuration
- ✅ MySQL dependencies in requirements.txt
- ✅ Database setup script
- ✅ Updated database examples
- ✅ Laravel-like command interface