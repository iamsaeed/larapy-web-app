"""PostController"""

from larapy import Response
from flask import render_template, request, redirect, url_for
from larapy.http.concerns.validates_requests import Controller
from app.Models.Post import Post


class PostController(Controller):
    """PostController class"""
    
    def __init__(self):
        super().__init__()
    
    def index(self):
        """Display a listing of the resource"""
        # posts = Post.all()
        return render_template('posts/index.html')
    
    def create(self):
        """Show the form for creating a new resource"""
        return render_template('posts/create.html')
    
    def store(self):
        """Store a newly created resource in storage"""
        # Validate request
        data = self.validate_request({
            'name': 'required|string|max:255',
            # Add your validation rules here
        })
        
        # Create new post
        # post = Post.create(data)
        
        # Redirect with success message
        return redirect(url_for('posts.index'))
    
    def show(self, id):
        """Display the specified resource"""
        # post = Post.find_or_fail(id)
        return render_template('posts/show.html', id=id)
    
    def edit(self, id):
        """Show the form for editing the specified resource"""
        # post = Post.find_or_fail(id)
        return render_template('posts/edit.html', id=id)
    
    def update(self, id):
        """Update the specified resource in storage"""
        # Validate request
        data = self.validate_request({
            'name': 'required|string|max:255',
            # Add your validation rules here
        })
        
        # Update post
        # post = Post.find_or_fail(id)
        # post.update(data)
        
        # Redirect with success message
        return redirect(url_for('posts.show', id=id))
    
    def destroy(self, id):
        """Remove the specified resource from storage"""
        # post = Post.find_or_fail(id)
        # post.delete()
        
        # Redirect with success message
        return redirect(url_for('posts.index'))
