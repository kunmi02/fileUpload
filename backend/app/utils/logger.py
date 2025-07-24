"""
Logging configuration for the application.
Sets up a centralized logger that can be imported and used throughout the app.
"""
import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from ..config import LOG_LEVEL, LOG_FILE

# Create logs directory if it doesn't exist
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

# Configure the root logger
def setup_logger():
    """Configure the application logger"""
    # Create logger
    logger = logging.getLogger("csv_app")
    logger.setLevel(getattr(logging, LOG_LEVEL))
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Create file handler for rotating log files (10MB max, keep 5 backups)
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger

# Create and export the logger instance
logger = setup_logger()
