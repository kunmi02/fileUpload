"""
Configuration settings for the application.
Loads settings from environment variables with sensible defaults.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# File upload settings
# Default max file size: 10MB (in bytes)
MAX_UPLOAD_SIZE = int(os.getenv('MAX_UPLOAD_SIZE', 10 * 1024 * 1024))

# Directory settings
UPLOAD_DIR = os.getenv('UPLOAD_DIR', './uploads')
PARQUET_DIR = os.getenv('PARQUET_DIR', './parquet')

# Database settings
DB_PATH = os.getenv('DB_PATH', './metadata.db')

# Logging settings
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_DIR = os.getenv('LOG_DIR', './logs')
LOG_FILE = os.path.join(LOG_DIR, 'app.log')
