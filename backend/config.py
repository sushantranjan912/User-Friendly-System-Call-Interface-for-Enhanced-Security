import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'dev-jwt-secret')
    DATABASE_PATH = os.getenv('DATABASE_PATH', 'database/database.db')
    ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY', 'change-this-to-a-secure-key-in-production')
    
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
