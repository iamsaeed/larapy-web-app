"""Create users table migration"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'package-larapy'))

from larapy.database.migrations.migration import Migration


class CreateUsersTable(Migration):
    """Migration to create users table"""
    
    def up(self):
        """Run the migrations"""
        with self.schema.create('users') as table:
            table.id()
            table.string('name')
            table.string('email').unique()
            table.timestamp('email_verified_at').nullable()
            table.string('password')
            table.string('phone', 20).nullable()
            table.text('address').nullable()
            table.string('city', 100).nullable()
            table.string('state', 50).nullable()
            table.string('zip_code', 10).nullable()
            table.boolean('is_admin').default(False)
            table.json('metadata').nullable()
            table.timestamp('last_login_at').nullable()
            table.string('remember_token', 100).nullable()
            table.string('status', 20).default('active')
            table.timestamps()
    
    def down(self):
        """Reverse the migrations"""
        self.schema.drop_if_exists('users')