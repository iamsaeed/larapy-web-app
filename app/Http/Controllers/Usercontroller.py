"""Usercontroller"""

from larapy import Response\nfrom flask import render_template, request\nfrom larapy.http.concerns.validates_requests import Controller


class Usercontroller(Controller):
    """Usercontroller class"""
    
    def __init__(self):
        super().__init__()
    
    def index(self):
        """Display the main view"""
        return render_template('index.html')
    
    def show(self, id):
        """Display a specific resource"""
        return render_template('show.html', id=id)
