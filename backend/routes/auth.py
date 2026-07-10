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
    data = request.get_json() or {}
    
    # Validate input
    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '')
    role = data.get('role', 'user')
    
    # Validation
    if not validate_username(username):
        return error_response('Invalid username. Must be 3-20 characters with letters, numbers, or underscore.', 400)
    
    if not validate_email(email):
        return error_response('Invalid email format.', 400)
    
    if not validate_password(password):
        return error_response('Password must be at least 8 characters and include letters and numbers.', 400)
    
    if not validate_role(role):
        return error_response('Invalid role.', 400)
    
    # Check if user already exists
    existing_user = db.execute_query(
        'SELECT id FROM users WHERE username = ? OR email = ?',
        (username, email)
    )
    
    if existing_user:
        return error_response('Username or email already exists.', 409)
    
    password_hash = hash_password(password)
    
    try:
        user_id = db.execute_insert(
            'INSERT INTO users (username, email, password_hash, role) VALUES (?, ?, ?, ?)',
            (username, email, password_hash, role)
        )
        
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
        
    except Exception:
        return error_response('Registration failed due to a server error.', 500)

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user and return JWT token"""
    data = request.get_json() or {}
    
    email = data.get('email', '').strip()
    password = data.get('password', '')
    
    if not email or not password:
        return error_response('Email and password are required.', 400)
    
    client_ip = get_client_ip(request)
    
    users = db.execute_query(
        'SELECT id, username, email, password_hash, role FROM users WHERE email = ?',
        (email,)
    )
    
    if not users:
        db.execute_insert(
            'INSERT INTO logs (action_type, ip_address, status, details) VALUES (?, ?, ?, ?)',
            ('login', client_ip, 'failure', f'Failed login attempt for {email}')
        )
        return error_response('Invalid email or password.', 401)
    
    user = dict(users[0])
    
    if not verify_password(password, user['password_hash']):
        db.execute_insert(
            'INSERT INTO logs (user_id, action_type, ip_address, status, details) VALUES (?, ?, ?, ?, ?)',
            (user['id'], 'login', client_ip, 'failure', 'Invalid password')
        )
        return error_response('Invalid email or password.', 401)
    
    token = generate_token(user['id'], user['username'], user['role'])
    
    db.execute_insert(
        'INSERT INTO logs (user_id, action_type, ip_address, status, details) VALUES (?, ?, ?, ?, ?)',
        (user['id'], 'login', client_ip, 'success', 'User logged in')
    )
    
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
