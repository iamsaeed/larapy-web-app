"""Logging configuration for Larapy application"""

import os

config = {
    # Default log channel
    'default': os.environ.get('LOG_CHANNEL', 'single'),

    # Log channels
    'channels': {
        'stack': {
            'driver': 'stack',
            'channels': ['single', 'daily'],
        },

        'single': {
            'driver': 'single',
            'path': 'larapy.log',
            'level': os.environ.get('LOG_LEVEL', 'DEBUG'),
        },

        'daily': {
            'driver': 'daily',
            'path': 'larapy.log',
            'level': os.environ.get('LOG_LEVEL', 'DEBUG'),
            'days': 14,
        },

        'errorlog': {
            'driver': 'errorlog',
            'level': os.environ.get('LOG_LEVEL', 'DEBUG'),
        },

        'null': {
            'driver': 'null',
        },
    },
}