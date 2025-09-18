"""Database configuration"""

import os

# Default database connection
DEFAULT = os.getenv('DB_CONNECTION', 'mysql')

# Database connections
CONNECTIONS = {
    'sqlite': {
        'driver': 'sqlite',
        'database': os.getenv('DB_DATABASE', 'database/database.sqlite'),
        'prefix': '',
        'foreign_key_constraints': True,
    },

    'mysql': {
        'driver': 'mysql',
        'host': os.getenv('DB_HOST', '127.0.0.1'),
        'port': int(os.getenv('DB_PORT', '3306')),
        'database': os.getenv('DB_DATABASE', 'larapy'),
        'username': os.getenv('DB_USERNAME', 'root'),
        'password': os.getenv('DB_PASSWORD', 'root'),
        'charset': 'utf8mb4',
        'collation': 'utf8mb4_unicode_ci',
        'prefix': '',
        'strict': True,
        'engine': None,
    },

    'postgres': {
        'driver': 'postgres',
        'host': os.getenv('DB_HOST', '127.0.0.1'),
        'port': int(os.getenv('DB_PORT', '5432')),
        'database': os.getenv('DB_DATABASE', 'larapy'),
        'username': os.getenv('DB_USERNAME', 'postgres'),
        'password': os.getenv('DB_PASSWORD', ''),
        'charset': 'utf8',
        'prefix': '',
        'schema': 'public',
        'sslmode': 'prefer',
    },
}

# Migration settings
MIGRATIONS = {
    'table': 'migrations',
    'path': 'database/migrations',
}

# Seeds settings
SEEDS = {
    'path': 'database/seeders',
}