import os
import sys
from dotenv import load_dotenv

load_dotenv()

def _validate_secret_key(key_name: str) -> str:
    """Validate that a secret key is set and meets minimum security requirements."""
    value = os.getenv(key_name)
    if not value:
        print(f"FATAL: {key_name} environment variable is not set.", file=sys.stderr)
        sys.exit(1)
    if len(value) < 32:
        print(f"FATAL: {key_name} must be at least 32 characters.", file=sys.stderr)
        sys.exit(1)
    return value

class Config:
    SECRET_KEY = _validate_secret_key('SECRET_KEY')
    JWT_SECRET_KEY = _validate_secret_key('JWT_SECRET_KEY')
    DATABASE_PATH = os.getenv('DATABASE_PATH', 'database/database.db')
    ENCRYPTION_KEY = _validate_secret_key('ENCRYPTION_KEY')
    
    # JWT Configuration
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hour
    JWT_REFRESH_TOKEN_EXPIRES = 2592000  # 30 days
    
    # Security Settings
    ALLOWED_COMMANDS = [
        'ls', 'dir', 'pwd', 'whoami', 'date', 'echo',
        'ipconfig', 'hostname', 'systeminfo', 'tasklist'
    ]
    
    # Rate Limiting
    RATE_LIMIT_ENABLED = True
    MAX_REQUESTS_PER_MINUTE = 60
    
    # CORS Settings
    CORS_ORIGINS = ['http://localhost:5000', 'http://127.0.0.1:5000']
