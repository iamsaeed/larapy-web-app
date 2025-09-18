"""ApiController"""

from larapy import Response
from flask import jsonify, request
from larapy.http.concerns.validates_requests import Controller


class ApiController(Controller):
    """ApiController class"""
    
    def __init__(self):
        super().__init__()
    
    def index(self):
        """Return a JSON response"""
        return {
            'message': 'Hello from API',
            'status': 'success'
        }
    
    def show(self, id):
        """Return a specific resource as JSON"""
        return {
            'id': id,
            'message': f'Resource {id} details',
            'status': 'success'
        }
