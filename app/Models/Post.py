"""Post model example"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'package-larapy'))

from larapy.database.eloquent.model import Model
from datetime import datetime


class Post(Model):
    """Post model with relationships"""
    
    # Table name
    table = 'posts'
    
    # Enable timestamps
    timestamps = True
    
    # Mass assignable attributes
    fillable = [
        'title', 'content', 'user_id', 'status', 'published_at',
        'meta_title', 'meta_description', 'slug'
    ]
    
    # Attribute casting
    casts = {
        'published_at': 'datetime',
        'is_published': 'boolean',
        'metadata': 'json'
    }
    
    # Date attributes
    dates = ['published_at']
    
    # Relationships
    def user(self):
        """Post belongs to a user"""
        return self.belongs_to('User', 'user_id', 'id')
    
    def comments(self):
        """Post has many comments"""
        return self.has_many('Comment', 'post_id', 'id')
    
    def tags(self):
        """Post belongs to many tags"""
        return self.belongs_to_many('Tag', 'post_tags', 'post_id', 'tag_id')
    
    # Scopes
    def scope_published(self, query):
        """Scope for published posts"""
        return query.where('status', 'published').where_not_null('published_at')
    
    def scope_draft(self, query):
        """Scope for draft posts"""
        return query.where('status', 'draft')
    
    def scope_recent(self, query, days=30):
        """Scope for recent posts"""
        from datetime import timedelta
        cutoff = datetime.now() - timedelta(days=days)
        return query.where('created_at', '>=', cutoff)
    
    # Accessors
    def get_excerpt_attribute(self, value):
        """Get post excerpt"""
        if self.content:
            return self.content[:150] + ('...' if len(self.content) > 150 else '')
        return ''
    
    def get_reading_time_attribute(self, value):
        """Calculate reading time"""
        if self.content:
            word_count = len(self.content.split())
            return max(1, round(word_count / 200))  # Assume 200 WPM
        return 0
    
    # Mutators
    def set_title_attribute(self, value):
        """Set title and generate slug"""
        self.attributes['title'] = value
        if value:
            # Simple slug generation
            import re
            slug = re.sub(r'[^\w\s-]', '', value.lower())
            slug = re.sub(r'[-\s]+', '-', slug).strip('-')
            self.attributes['slug'] = slug
    
    # Methods
    def publish(self):
        """Publish the post"""
        self.status = 'published'
        self.published_at = datetime.now()
        self.save()
    
    def unpublish(self):
        """Unpublish the post"""
        self.status = 'draft'
        self.published_at = None
        self.save()
    
    def add_tag(self, tag):
        """Add a tag to the post"""
        return self.tags().attach(tag)
    
    def remove_tag(self, tag):
        """Remove a tag from the post"""
        return self.tags().detach(tag)
    
    def sync_tags(self, tag_ids):
        """Sync tags for the post"""
        return self.tags().sync(tag_ids)
    
    @classmethod
    def create_with_tags(cls, post_data, tag_ids=None):
        """Create post with tags"""
        post = cls.create(post_data)
        if tag_ids:
            post.sync_tags(tag_ids)
        return post
    
    @classmethod
    def search(cls, term):
        """Search posts by title or content"""
        return cls.query().where(
            lambda q: q.where('title', 'like', f'%{term}%')
                      .or_where('content', 'like', f'%{term}%')
        )
    
    def __str__(self):
        return f"Post(id={self.id}, title={self.title}, user_id={self.user_id})"