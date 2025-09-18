"""Create posts table migration"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'package-larapy'))

from larapy.database.migrations.migration import Migration


class CreatePostsTable(Migration):
    """Migration to create posts table"""
    
    def up(self):
        """Run the migrations"""
        with self.schema.create('posts') as table:
            table.id()
            table.string('title')
            table.string('slug').unique()
            table.text('content')
            table.string('meta_title').nullable()
            table.text('meta_description').nullable()
            table.foreign_id('user_id').constrained('users').on_delete('cascade')
            table.string('status', 20).default('draft')
            table.timestamp('published_at').nullable()
            table.json('metadata').nullable()
            table.timestamps()
            
            # Add indexes
            table.index(['status', 'published_at'])
            table.index('user_id')
    
    def down(self):
        """Reverse the migrations"""
        self.schema.drop_if_exists('posts')