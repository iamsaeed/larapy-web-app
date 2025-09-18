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
    
    def api_data(self):
        """API endpoint returning JSON data"""
        return {
            'message': 'Hello from Larapy API',
            'version': '1.0.0',
            'status': 'success',
            'data': [
                {'id': 1, 'name': 'Item 1'},
                {'id': 2, 'name': 'Item 2'},
                {'id': 3, 'name': 'Item 3'},
            ]
        }
    