import subprocess
from datetime import datetime

def execute_system_call(command):
    """Execute a system call and return output"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=10
        )
        
        return {
            'status': 'success' if result.returncode == 0 else 'failure',
            'output': result.stdout if result.returncode == 0 else result.stderr,
            'return_code': result.returncode
        }
    except subprocess.TimeoutExpired:
        return {
            'status': 'failure',
            'output': 'Command execution timed out',
            'return_code': -1
        }
    except Exception as e:
        return {
            'status': 'failure',
            'output': str(e),
            'return_code': -1
        }

def format_log_entry(action_type, user_id, ip_address, status, details):
    """Format a log entry"""
    return {
        'action_type': action_type,
        'user_id': user_id,
        'ip_address': ip_address,
        'status': status,
        'details': details,
        'timestamp': datetime.utcnow().isoformat()
    }

def get_client_ip(request):
    """Get client IP address from request"""
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0]
    return request.remote_addr

def success_response(data, message='Success'):
    """Format success response"""
    return {
        'success': True,
        'message': message,
        'data': data
    }

def error_response(message, code=400, data=None):
    """Format error response"""
    response = {
        'success': False,
        'error': message
    }
    if data:
        response['data'] = data
    return response, code
