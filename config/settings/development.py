"""Development settings."""
from .base import *  # noqa: F401, F403

DEBUG = True

INSTALLED_APPS += ['django_extensions']  # noqa: F405

# Less strict security for development
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# Show all SQL queries
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
