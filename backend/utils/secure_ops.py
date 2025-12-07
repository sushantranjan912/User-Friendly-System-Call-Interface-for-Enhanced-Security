import os
import subprocess
from datetime import datetime
from cryptography.fernet import Fernet
from database.db_connection import Database
from config import Config
from werkzeug.utils import secure_filename

db = Database(Config.DATABASE_PATH)

# Initialize encryption
# Ensure key is valid base64 url-safe, if not generate one (for dev)
try:
    cipher_suite = Fernet(Config.ENCRYPTION_KEY.encode())
except:
    # Fallback for dev if key is invalid
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)
    print(f"WARNING: Generated new encryption key: {key.decode()}")

SANDBOX_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ssci_files')

def encrypt_data(data):
    """Encrypt string data"""
    if not data:
        return ""
    return cipher_suite.encrypt(data.encode()).decode()

def decrypt_data(data):
    """Decrypt string data"""
    if not data:
        return ""
    try:
        return cipher_suite.decrypt(data.encode()).decode()
    except:
        return "[Decryption Failed]"

def log_secure_action(user_id, action_type, ip_address, status, details):
    """Log action with encrypted details"""
    encrypted_details = encrypt_data(details)
    
    db.execute_insert(
        'INSERT INTO logs (user_id, action_type, ip_address, status, details) VALUES (?, ?, ?, ?, ?)',
        (user_id, action_type, ip_address, status, encrypted_details)
    )

def is_safe_path(path):
    """Ensure path is within sandbox directory"""
    if not os.path.exists(SANDBOX_DIR):
        os.makedirs(SANDBOX_DIR)
    
    # Resolve absolute path
    abs_path = os.path.abspath(os.path.join(SANDBOX_DIR, path))
    # Check if it starts with sandbox path
    return abs_path.startswith(os.path.abspath(SANDBOX_DIR))

def secure_open(path, mode, user_id, ip_address):
    """Securely open a file (conceptually, returns path if safe)"""
    filename = secure_filename(path)
    
    if not is_safe_path(filename):
        log_secure_action(user_id, 'secure_open', ip_address, 'failure', f'Path traversal attempt: {path}')
        raise ValueError("Invalid filename or path traversal attempt.")
    
    return os.path.join(SANDBOX_DIR, filename)

def secure_read(path, user_id, ip_address):
    """Securely read a file"""
    try:
        file_path = secure_open(path, 'r', user_id, ip_address)
        
        if not os.path.exists(file_path):
            log_secure_action(user_id, 'secure_read', ip_address, 'failure', f'File not found: {path}')
            raise FileNotFoundError("File not found.")
            
        with open(file_path, 'r') as f:
            content = f.read()
            
        log_secure_action(user_id, 'secure_read', ip_address, 'success', f'Read file: {path}')
        return content
    except Exception as e:
        log_secure_action(user_id, 'secure_read', ip_address, 'failure', f'Error reading {path}: {str(e)}')
        raise e

def secure_write(path, content, user_id, ip_address):
    """Securely write to a file"""
    try:
        file_path = secure_open(path, 'w', user_id, ip_address)
        
        with open(file_path, 'w') as f:
            f.write(content)
            
        log_secure_action(user_id, 'secure_write', ip_address, 'success', f'Wrote to file: {path}')
        return True
    except Exception as e:
        log_secure_action(user_id, 'secure_write', ip_address, 'failure', f'Error writing {path}: {str(e)}')
        raise e

def secure_delete(path, user_id, ip_address):
    """Securely delete a file"""
    try:
        file_path = secure_open(path, 'd', user_id, ip_address)
        
        if not os.path.exists(file_path):
            log_secure_action(user_id, 'secure_delete', ip_address, 'failure', f'File not found: {path}')
            raise FileNotFoundError("File not found.")
            
        os.remove(file_path)
        log_secure_action(user_id, 'secure_delete', ip_address, 'success', f'Deleted file: {path}')
        return True
    except Exception as e:
        log_secure_action(user_id, 'secure_delete', ip_address, 'failure', f'Error deleting {path}: {str(e)}')
        raise e

def secure_execute(command, user_id, ip_address):
    """Securely execute a command"""
    # Whitelist check
    cmd_parts = command.split()
    base_cmd = cmd_parts[0] if cmd_parts else ""
    
    if base_cmd not in Config.ALLOWED_COMMANDS:
        log_secure_action(user_id, 'secure_execute', ip_address, 'failure', f'Unauthorized command: {command}')
        raise ValueError("Command not allowed.")
        
    try:
        # Execute
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=10
        )
        
        status = 'success' if result.returncode == 0 else 'failure'
        output = result.stdout if result.returncode == 0 else result.stderr
        
        log_secure_action(user_id, 'secure_execute', ip_address, status, f'Executed: {command}')
        
        return {
            'status': status,
            'output': output,
            'return_code': result.returncode
        }
    except Exception as e:
        log_secure_action(user_id, 'secure_execute', ip_address, 'failure', f'Execution error: {str(e)}')
        raise e
