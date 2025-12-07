import re
from config import Config

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_username(username):
    """Validate username (alphanumeric, 3-20 chars)"""
    if not username or len(username) < 3 or len(username) > 20:
        return False
    return re.match(r'^[a-zA-Z0-9_]+$', username) is not None

def validate_password(password):
    """Validate password strength (min 8 chars, at least 1 letter and 1 number)"""
    if not password or len(password) < 8:
        return False
    has_letter = re.search(r'[a-zA-Z]', password)
    has_number = re.search(r'[0-9]', password)
    return has_letter and has_number

def sanitize_command(command):
    """Sanitize and validate system command"""
    # Remove dangerous characters
    command = command.strip()
    
    # Check if command is in allowed list
    base_command = command.split()[0] if command else ''
    
    if base_command not in Config.ALLOWED_COMMANDS:
        return None
    
    # Remove potentially dangerous characters
    dangerous_chars = [';', '&', '|', '>', '<', '`', '$', '(', ')']
    for char in dangerous_chars:
        if char in command:
            return None
    
    return command

def validate_role(role):
    """Validate user role"""
    return role in ['admin', 'user', 'viewer']
