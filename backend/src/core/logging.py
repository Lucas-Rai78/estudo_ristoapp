import logging.config
import os

# ./logs in system root
os.makedirs("logs", exist_ok=True)

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    
    'formatters': {
        'pattern': {
            'format': '%(asctime)s - %(levelname)s - [%(name)s] - %(message)s'
        },
        'details': {
            'format': '%(asctime)s - %(levelname)s - [%(name)s] (%(filename)s:%(lineno)d) - %(message)s'
        }
    },
    
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'pattern',
            'level': 'INFO',
        },
        'auth_file': {
            'class': 'logging.FileHandler',
            'filename': 'logs/auth.log',
            'formatter': 'details',
            'level': 'DEBUG', # Auth logging
        },
        'inventory_file': {
            'class': 'logging.FileHandler',
            'filename': 'logs/inventory.log',
            'formatter': 'details',
            'level': 'INFO',
        },
        'main_file': {
            'class': 'logging.FileHandler',
            'filename': 'logs/main.log',
            'formatter': 'pattern',
            'level': 'WARNING', # Warnings and global alerts
        }
    },
    
    'loggers': {
        # Config for everything inside src/modules/auth/
        'modules.auth': {
            'handlers': ['console', 'auth_file'],
            'level': 'DEBUG',
            'propagate': False 
        },
        
        # Config for everything inside src/modules/inventory/
        'modules.inventory': {
            'handlers': ['console', 'inventory_file'],
            'level': 'INFO',
            'propagate': False
        },
        
        # Config for everything inside src/core/
        'core': {
            'handlers': ['console', 'main_file'],
            'level': 'INFO',
            'propagate': False
        }
    },
    
    'root': {
        'handlers': ['console', 'main_file'],
        'level': 'WARNING',
    }
}

def setup_logging():
    """Inicializa as configurações de log da aplicação."""
    logging.config.dictConfig(LOGGING_CONFIG)