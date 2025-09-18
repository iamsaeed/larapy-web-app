"""
Security Configuration for MyApp

Laravel-style security configuration integrated with Larapy security middleware.
"""

import os
from pathlib import Path


def get_security_config():
    """Get security configuration for the application"""
    
    # Get APP_KEY from environment or generate one
    app_key = os.getenv('APP_KEY')
    if not app_key:
        # In production, this should be set in .env
        app_key = 'base64:' + 'your-32-character-secret-key-here'
    
    # Check if we're in development mode
    is_development = os.getenv('APP_ENV', 'production') == 'local' or os.getenv('APP_DEBUG', 'false').lower() == 'true'
    
    return {
        # Encryption
        'encryption': {
            'key': app_key,
            'cipher': 'fernet',
        },
        
        # CSRF Protection
        'csrf': {
            'enabled': True,
            'cookie_name': 'XSRF-TOKEN',
            'header_name': 'X-CSRF-TOKEN', 
            'field_name': '_token',
            'exclude': [
                'api/*',
                'webhooks/*',
            ]
        },
        
        # CORS
        'cors': {
            'paths': ['api/*'],
            'allowed_origins': ['*'],
            'allowed_methods': ['*'],
            'allowed_headers': ['*'],
            'exposed_headers': [],
            'max_age': 0,
            'supports_credentials': False,
        },
        
        # Rate Limiting
        'rate_limiting': {
            'default': '60,1',    # 60 requests per minute
            'api': '1000,60',     # 1000 per hour
            'login': '5,1',       # 5 login attempts per minute
        },
        
        # Cookie Encryption
        'cookies': {
            'encrypt': True,
            'exclude': [
                'cookie_consent',
                'session',
            ]
        },
        
        # Security Headers
        'security_headers': {
            'x_frame_options': 'SAMEORIGIN',
            'x_content_type_options': 'nosniff',
            'x_xss_protection': '1; mode=block',
            'strict_transport_security': 'max-age=31536000; includeSubDomains' if not is_development else None,
            'content_security_policy': None if is_development else "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval' https://unpkg.com; style-src 'self' 'unsafe-inline' https://unpkg.com; img-src 'self' data: https:; font-src 'self' https:; connect-src 'self' ws: wss:;",
            'referrer_policy': 'strict-origin-when-cross-origin',
            'permissions_policy': 'geolocation=(), microphone=(), camera=()',
        },
        
        # Password Hashing
        'hashing': {
            'driver': 'bcrypt',
            'bcrypt': {
                'rounds': 12,
            },
        },
        
        # Authentication
        'auth': {
            'defaults': {
                'guard': 'web',
            },
            'guards': {
                'web': {
                    'driver': 'session',
                    'provider': 'users',
                },
                'api': {
                    'driver': 'token',
                    'provider': 'users',
                },
            },
        },
    }