"""
Home Controller - Handles main application pages with view rendering
"""

from larapy import Response
from flask import render_template
from app.Models.User import User
import json

class HomeController:
    """Main controller for homepage and basic routes"""
    
    def index(self):
        """Homepage with modern UI"""
        user = {
            'id' : 1,
            'name': 'John Doe',
            'email': 'john@doe.com'
        }
        return render_template('index.html', 
            user=user,
            title='Welcome to Larapy',
            message='Laravel concepts in Python Flask'
        )
    

    def contact(self):
        """Contact page with interactive form"""
        return render_template('contact.html',
            title='Contact Us'
        )
    