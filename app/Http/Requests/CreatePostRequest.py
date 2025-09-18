"""
CreatePostRequest

Form request class for createpost validation and authorization.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'package-larapy'))

from larapy.http.form_request import FormRequest
from typing import Dict, Union, List, Optional


class CreatePostRequest(FormRequest):
    """
    CreatePostRequest
    
    Handles validation and authorization for createpost requests.
    """
    
    def authorize(self) -> bool:
        """
        Determine if the user is authorized to make this request
        
        Returns:
            True if the user is authorized, False otherwise
        """
        # Add your authorization logic here
        # Example: return self.user() and self.user().can('create-createpost')
        return True
    
    def rules(self) -> Dict[str, Union[str, List[str]]]:
        """
        Get the validation rules that apply to the request
        
        Returns:
            Dictionary of validation rules
        """
        return {
            # Define your validation rules here
            # Example:
            # 'name': 'required|string|max:255',
            # 'email': 'required|email|unique:users,email',
            # 'password': 'required|string|min:8|confirmed',
        }
    
    def messages(self) -> Dict[str, str]:
        """
        Get custom validation messages
        
        Returns:
            Dictionary of custom validation messages
        """
        return {
            # Define custom validation messages here
            # Example:
            # 'name.required': 'The name field is required.',
            # 'email.email': 'Please provide a valid email address.',
            # 'password.min': 'The password must be at least 8 characters.',
        }
    
    def attributes(self) -> Dict[str, str]:
        """
        Get custom attribute names for validation errors
        
        Returns:
            Dictionary of custom attribute names
        """
        return {
            # Define custom attribute names here
            # Example:
            # 'email': 'email address',
            # 'first_name': 'given name',
        }
    
    def prepare_for_validation(self):
        """
        Prepare the data for validation
        
        This method is called before validation occurs.
        Use it to modify or clean the input data.
        """
        # Add any data preparation logic here
        # Example:
        # self.merge([
        #     'slug': self.input('name', '').lower().replace(' ', '-')
        # ])
        pass
    
    def with_validator(self, validator):
        """
        Configure the validator instance
        
        Args:
            validator: The validator instance
        """
        # Add custom validation logic here
        # Example:
        # validator.after(lambda: self._validate_business_rules())
        pass
    
    def failed_validation(self, validator):
        """
        Handle a failed validation attempt
        
        Args:
            validator: The validator instance that failed
        """
        # Custom logic for handling validation failures
        # This is called before the ValidationException is thrown
        pass
