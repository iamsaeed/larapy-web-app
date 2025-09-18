"""OrderController"""

from larapy import Response
from flask import render_template, request, redirect, url_for
from larapy.http.concerns.validates_requests import Controller


class OrderController(Controller):
    """OrderController class"""
    
    def __init__(self):
        super().__init__()
    
    def index(self):
        """Display a listing of the resource"""
        # items = Model.all()
        return render_template('items/index.html')
    
    def create(self):
        """Show the form for creating a new resource"""
        return render_template('items/create.html')
    
    def store(self):
        """Store a newly created resource in storage"""
        # Validate request
        data = self.validate_request({
            'name': 'required|string|max:255',
            # Add your validation rules here
        })
        
        # Create new item
        # item = Model.create(data)
        
        # Redirect with success message
        return redirect(url_for('items.index'))
    
    def show(self, id):
        """Display the specified resource"""
        # item = Model.find_or_fail(id)
        return render_template('items/show.html', id=id)
    
    def edit(self, id):
        """Show the form for editing the specified resource"""
        # item = Model.find_or_fail(id)
        return render_template('items/edit.html', id=id)
    
    def update(self, id):
        """Update the specified resource in storage"""
        # Validate request
        data = self.validate_request({
            'name': 'required|string|max:255',
            # Add your validation rules here
        })
        
        # Update item
        # item = Model.find_or_fail(id)
        # item.update(data)
        
        # Redirect with success message
        return redirect(url_for('items.show', id=id))
    
    def destroy(self, id):
        """Remove the specified resource from storage"""
        # item = Model.find_or_fail(id)
        # item.delete()
        
        # Redirect with success message
        return redirect(url_for('items.index'))
