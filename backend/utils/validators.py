import re
import os
from werkzeug.utils import secure_filename as werkzeug_secure_filename
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
    return bool(has_letter and has_number)

def validate_filename(filename):
    """Validate filename for safety and allowed extension."""
    if not filename:
        return False

    # Basic length check
    if len(filename) > 255:
        return False

    # Disallow traversal patterns and path separators
    if '..' in filename or '/' in filename or '\\' in filename:
        return False

    # Use werkzeug secure_filename to normalize and ensure no weird chars
    safe = werkzeug_secure_filename(filename)
    if not safe:
        return False

    # Ensure extension is allowed (if present)
    ext = os.path.splitext(safe)[1].lstrip('.').lower()
    if ext:
        allowed = getattr(Config, 'ALLOWED_UPLOAD_EXTENSIONS', None)
        if allowed is not None and ext not in allowed:
            return False

    return True

def validate_filesize(size_bytes):
    """Validate that size is within configured limits (bytes)."""
    if size_bytes is None:
        return False
    max_size = getattr(Config, 'MAX_UPLOAD_SIZE', None)
    if max_size is None:
        return True
    try:
        return int(size_bytes) <= int(max_size)
    except Exception:
        return False

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
