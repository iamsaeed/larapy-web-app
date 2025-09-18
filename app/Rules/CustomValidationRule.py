"""
CustomValidationRule

Custom validation rule for customvalidation validation.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'package-larapy'))

from larapy.validation.rule import Rule
from typing import Any, Optional


class CustomValidationRule(Rule):
    """
    CustomValidationRule
    
    Custom validation rule for customvalidation validation.
    """
    
    def __init__(self, *args, **kwargs):
        """
        Initialize the validation rule
        
        Args:
            *args: Positional arguments for the rule
            **kwargs: Keyword arguments for the rule
        """
        super().__init__()
        self.args = args
        self.kwargs = kwargs
    
    def passes(self, attribute: str, value: Any) -> bool:
        """
        Determine if the validation rule passes
        
        Args:
            attribute: The attribute name being validated
            value: The value being validated
            
        Returns:
            True if validation passes, False otherwise
        """
        # Add your validation logic here
        # Example validations:
        
        # Check if value is not None or empty
        if value is None or (isinstance(value, str) and not value.strip()):
            return False
        
        # Example: String length validation
        # if isinstance(value, str):
        #     min_length = self.kwargs.get('min_length', 1)
        #     max_length = self.kwargs.get('max_length', 255)
        #     return min_length <= len(value) <= max_length
        
        # Example: Numeric range validation
        # if isinstance(value, (int, float)):
        #     min_value = self.kwargs.get('min_value', 0)
        #     max_value = self.kwargs.get('max_value', 100)
        #     return min_value <= value <= max_value
        
        # Example: Email format validation
        # if isinstance(value, str):
        #     import re
        #     email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        #     return re.match(email_pattern, value) is not None
        
        # Example: Custom business logic
        # if isinstance(value, str):
        #     forbidden_words = ['spam', 'test', 'admin']
        #     return not any(word in value.lower() for word in forbidden_words)
        
        # Default: return True (passes validation)
        return True
    
    def message(self) -> str:
        """
        Get the validation error message
        
        Returns:
            The validation error message
        """
        # Return a custom error message
        return f"The :attribute field does not pass customvalidation validation."
        
        # You can also return dynamic messages based on the rule parameters
        # Example:
        # if 'min_length' in self.kwargs:
        #     return f"The :attribute must be at least {self.kwargs['min_length']} characters."
        # return "The :attribute is invalid."
    
    def __str__(self) -> str:
        """
        Get the string representation of the rule
        
        Returns:
            String representation of the rule
        """
        return f"customvalidation"
    
    # Optional: Add additional methods for complex validation
    def set_parameters(self, parameters: list) -> 'Rule':
        """
        Set rule parameters from validation string
        
        Args:
            parameters: List of parameters from validation rule string
            
        Returns:
            Self for method chaining
        """
        # Parse parameters if your rule accepts them
        # Example: "custom_rule:min_length=5,max_length=100"
        for param in parameters:
            if '=' in param:
                key, value = param.split('=', 1)
                try:
                    # Try to convert to int/float if possible
                    if value.isdigit():
                        value = int(value)
                    elif value.replace('.', '').isdigit():
                        value = float(value)
                    self.kwargs[key] = value
                except ValueError:
                    self.kwargs[key] = value
            else:
                self.args = self.args + (param,)
        
        return self
    
    def get_size(self, value: Any) -> Optional[int]:
        """
        Get the size of the value for size-based validation
        
        Args:
            value: The value to get size for
            
        Returns:
            Size of the value or None
        """
        if isinstance(value, str):
            return len(value)
        elif isinstance(value, (list, tuple, dict)):
            return len(value)
        elif isinstance(value, (int, float)):
            return value
        return None
