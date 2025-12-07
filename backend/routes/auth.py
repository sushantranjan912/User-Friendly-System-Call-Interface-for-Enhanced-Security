from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from database.db_connection import Database
from utils.auth_utils import hash_password, verify_password, generate_token
from utils.validators import validate_email, validate_username, validate_password, validate_role
from utils.helpers import get_client_ip, success_response, error_response
from config import Config

auth_bp = Blueprint('auth', __name__)
db = Database(Config.DATABASE_PATH)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()
    
    # Validate input
    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '')
    role = data.get('role', 'user')
    
    # Validation
    if not validate_username(username):
        return error_response('Invalid username. Must be 3-20 alphanumeric characters.')
    
    if not validate_email(email):
        return error_response('Invalid email format.')
    
    if not validate_password(password):
        return error_response('Password must be at least 8 characters with letters and numbers.')
    
    if not validate_role(role):
        return error_response('Invalid role.')
    
    # Check if user already exists
    existing_user = db.execute_query(
        'SELECT id FROM users WHERE username = ? OR email = ?',
        (username, email)
    )
    
    if existing_user:
        return error_response('Username or email already exists.')
    
    # Hash password and create user
    password_hash = hash_password(password)
    
    try:
        user_id = db.execute_insert(
            'INSERT INTO users (username, email, password_hash, role) VALUES (?, ?, ?, ?)',
            (username, email, password_hash, role)
        )
        
        # Log the registration
        db.execute_insert(
            'INSERT INTO logs (user_id, action_type, ip_address, status, details) VALUES (?, ?, ?, ?, ?)',
            (user_id, 'register', get_client_ip(request), 'success', f'User {username} registered')
        )
        
        return jsonify(success_response({
            'user_id': user_id,
            'username': username,
            'email': email,
            'role': role
        }, 'Registration successful')), 201
        
    except Exception as e:
        return error_response(f'Registration failed: {str(e)}', 500)

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user and return JWT token"""
    data = request.get_json()
    
    username = data.get('username', '').strip()
    password = data.get('password', '')
    
    if not username or not password:
        return error_response('Username and password are required.')
    
    client_ip = get_client_ip(request)
    
    # TODO: Re-enable after fixing database schema issue
    # # Check for temporary block (5 failed attempts in last 15 minutes)
    # recent_failures = db.execute_query(
    #     '''SELECT COUNT(*) as count FROM login_attempts 
    #        WHERE ip_address = ? AND success = 0 
    #        AND attempt_time >= datetime('now', '-15 minutes')''',
    #     (client_ip,)
    # )
    # 
    # if recent_failures and recent_failures[0]['count'] >= 5:
    #     # Log suspicious activity
    #     db.execute_insert(
    #         'INSERT INTO logs (action_type, ip_address, status, details) VALUES (?, ?, ?, ?)',
    #         ('login_blocked', client_ip, 'suspicious', f'Temporary block due to repeated failed attempts: {username}')
    #     )
    #     return error_response('Too many failed attempts. Please try again later.', 429)
    
    # Get user from database
    users = db.execute_query(
        'SELECT id, username, email, password_hash, role FROM users WHERE username = ?',
        (username,)
    )
    
    if not users:
        # Log failed login attempt
        db.execute_insert(
            'INSERT INTO logs (action_type, ip_address, status, details) VALUES (?, ?, ?, ?)',
            ('login', client_ip, 'failure', f'Failed login attempt for {username}')
        )
        # # Record failed attempt for blocking
        # db.execute_insert(
        #     'INSERT INTO login_attempts (ip_address, username, success) VALUES (?, ?, 0)',
        #     (client_ip, username)
        # )
        return error_response('Invalid credentials.')
    
    user = dict(users[0])
    
    # Verify password
    if not verify_password(password, user['password_hash']):
        # Log failed login attempt
        db.execute_insert(
            'INSERT INTO logs (user_id, action_type, ip_address, status, details) VALUES (?, ?, ?, ?, ?)',
            (user['id'], 'login', client_ip, 'failure', 'Invalid password')
        )
        # # Record failed attempt for blocking
        # db.execute_insert(
        #     'INSERT INTO login_attempts (ip_address, username, success) VALUES (?, ?, 0)',
        #     (client_ip, username)
        # )
        return error_response('Invalid credentials.')
    
    # Generate token
    token = generate_token(user['id'], user['username'], user['role'])
    
    # Log successful login
    db.execute_insert(
        'INSERT INTO logs (user_id, action_type, ip_address, status, details) VALUES (?, ?, ?, ?, ?)',
        (user['id'], 'login', client_ip, 'success', 'User logged in')
    )
    
    # # Record successful attempt (optional, but good for tracking)
    # db.execute_insert(
    #     'INSERT INTO login_attempts (ip_address, username, success) VALUES (?, ?, 1)',
    #     (client_ip, username)
    # )
    
    return jsonify(success_response({
        'token': token,
        'user': {
            'id': user['id'],
            'username': user['username'],
            'email': user['email'],
            'role': user['role']
        }
    }, 'Login successful'))

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Logout user (client-side token removal)"""
    # In a stateless JWT system, logout is handled client-side
    # This endpoint is for logging purposes
    
    auth_header = request.headers.get('Authorization', '')
    if auth_header:
        from utils.auth_utils import decode_token
        token = auth_header.split(' ')[1] if ' ' in auth_header else ''
        payload = decode_token(token)
        
        if payload:
            db.execute_insert(
                'INSERT INTO logs (user_id, action_type, ip_address, status, details) VALUES (?, ?, ?, ?, ?)',
                (payload['user_id'], 'logout', get_client_ip(request), 'success', 'User logged out')
            )
    
    return jsonify(success_response(None, 'Logout successful'))
