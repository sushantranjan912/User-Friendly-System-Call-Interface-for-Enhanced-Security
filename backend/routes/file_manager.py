from flask import Blueprint, request, jsonify, send_file
import os
import shutil
import time
import json
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from database.db_connection import Database
from utils.auth_utils import token_required, role_required
from utils.helpers import get_client_ip, success_response, error_response
from utils.secure_ops import secure_read, secure_write, secure_delete, is_safe_path, SANDBOX_DIR
from config import Config

file_manager_bp = Blueprint('file_manager', __name__)
db = Database(Config.DATABASE_PATH)

@file_manager_bp.route('/', methods=['GET'])
@token_required
def list_files(current_user):
    """List files in sandbox directory with permissions"""
    try:
        if not os.path.exists(SANDBOX_DIR):
            os.makedirs(SANDBOX_DIR)
            
        files = []
        
        # Load all permissions once
        permissions_file = os.path.join(os.path.dirname(__file__), '..', 'file_permissions.json')
        all_permissions = {}
        if os.path.exists(permissions_file):
            import json
            with open(permissions_file, 'r') as f:
                try:
                    all_permissions = json.load(f)
                except:
                    pass

        for filename in os.listdir(SANDBOX_DIR):
            file_path = os.path.join(SANDBOX_DIR, filename)
            if os.path.isfile(file_path):
                stats = os.stat(file_path)
                
                # Get permissions for this file
                perms = all_permissions.get(filename, {
                    'view': True,
                    'download': True,
                    'edit': False,
                    'delete': False,
                    'owner': None
                })
                
                files.append({
                    'name': filename,
                    'size': stats.st_size,
                    'modified': stats.st_mtime,
                    'permissions': perms
                })
        
        return jsonify(success_response({'files': files}))
    except Exception as e:
        return error_response(f'Failed to list files: {str(e)}', 500)

@file_manager_bp.route('/', methods=['POST'])
@token_required
def create_file(current_user):
    """Create a new file"""
    data = request.get_json()
    filename = data.get('filename', '').strip()
    content = data.get('content', '')
    
    if not filename:
        return error_response('Filename is required.')
    
    try:
        # Check if file exists to prevent overwrite if not intended (though secure_write overwrites)
        # But here we are "creating".
        # secure_write handles path safety and logging.
        secure_write(filename, content, current_user['user_id'], get_client_ip(request))
        return jsonify(success_response(None, 'File created successfully'))
    except Exception as e:
        return error_response(f'Failed to create file: {str(e)}', 500)

@file_manager_bp.route('/<filename>', methods=['GET'])
@token_required
def read_file(current_user, filename):
    """Read file content"""
    try:
        filename = secure_filename(filename)
        if not is_safe_path(filename):
            return error_response('Invalid filename.')
        
        file_path = os.path.join(SANDBOX_DIR, filename)
        if not os.path.exists(file_path):
            return error_response('File not found.', 404)
        
        # Check view permission
        permissions = get_file_permissions(filename)
        if not permissions.get('view', True):
            return error_response('You do not have permission to view this file.', 403)
            
        # Check File Lock
        if permissions.get('is_locked', False):
            passcode = request.headers.get('X-File-Passcode')
            if not passcode or not check_password_hash(permissions.get('lock_hash', ''), passcode):
                return error_response('File is locked. Passcode required.', 403, {'locked': True})
        
        # Try to read as text first
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Log the action
            from utils.secure_ops import log_secure_action
            log_secure_action(
                current_user['user_id'],
                'file_read',
                get_client_ip(request),
                'success',
                f'Read file: {filename}'
            )
            
            return jsonify(success_response({'content': content, 'filename': filename, 'is_binary': False}))
        except UnicodeDecodeError:
            # Binary file - return info that it's binary
            file_size = os.path.getsize(file_path)
            return jsonify(success_response({
                'content': f'[Binary File - {filename}]\nSize: {file_size} bytes\nThis file cannot be viewed as text. Please download it to view.',
                'filename': filename,
                'is_binary': True
            }))
            
    except Exception as e:
        return error_response(f'Failed to read file: {str(e)}', 500)

@file_manager_bp.route('/<filename>', methods=['PUT'])
@token_required
def update_file(current_user, filename):
    """Update file content"""
    data = request.get_json()
    content = data.get('content', '')
    
    try:
        permissions = get_file_permissions(filename)
        
        # Check File Lock
        if permissions.get('is_locked', False):
            passcode = request.headers.get('X-File-Passcode')
            if not passcode or not check_password_hash(permissions.get('lock_hash', ''), passcode):
                return error_response('File is locked. Passcode required.', 403, {'locked': True})

        # Check edit permission (admin bypasses this check)
        if current_user['role'] != 'admin':
            if not permissions.get('edit', False):
                return error_response('You do not have permission to edit this file.', 403)
        
        secure_write(filename, content, current_user['user_id'], get_client_ip(request))
        return jsonify(success_response(None, 'File updated successfully'))
    except Exception as e:
        return error_response(f'Failed to update file: {str(e)}', 500)

@file_manager_bp.route('/<filename>', methods=['DELETE'])
@token_required
def delete_file(current_user, filename):
    """Delete file (Move to Recycle Bin)"""
    try:
        permissions = get_file_permissions(filename)
        
        # Check File Lock
        if permissions.get('is_locked', False):
            passcode = request.headers.get('X-File-Passcode')
            if not passcode or not check_password_hash(permissions.get('lock_hash', ''), passcode):
                return error_response('File is locked. Passcode required.', 403, {'locked': True})

        # Check delete permission (admin bypasses this check)
        if current_user['role'] != 'admin':
            if not permissions.get('delete', False):
                return error_response('You do not have permission to delete this file.', 403)
        
        file_path = os.path.join(SANDBOX_DIR, filename)
        if not os.path.exists(file_path):
            return error_response('File not found.', 404)
            
        # Recycle Bin Logic
        RECYCLE_BIN_DIR = os.path.join(os.path.dirname(SANDBOX_DIR), 'recycle_bin')
        if not os.path.exists(RECYCLE_BIN_DIR):
            os.makedirs(RECYCLE_BIN_DIR)
            
        # Generate unique name for recycle bin
        timestamp = int(time.time())
        recycle_filename = f"{timestamp}_{filename}"
        recycle_path = os.path.join(RECYCLE_BIN_DIR, recycle_filename)
        
        # Get current permissions to save in metadata
        current_permissions = get_file_permissions(filename)
        
        # Move file
        shutil.move(file_path, recycle_path)
        
        # Update Recycle Bin Metadata
        metadata_file = os.path.join(RECYCLE_BIN_DIR, 'metadata.json')
        metadata = {}
        if os.path.exists(metadata_file):
            try:
                with open(metadata_file, 'r') as f:
                    metadata = json.load(f)
            except:
                pass
                
        metadata[recycle_filename] = {
            'original_name': filename,
            'deleted_at': timestamp,
            'deleted_by': current_user['username'],
            'permissions': current_permissions
        }
        
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        # Remove permissions entry from file_permissions.json
        permissions_file = os.path.join(os.path.dirname(__file__), '..', 'file_permissions.json')
        try:
            with open(permissions_file, 'r') as f:
                all_permissions = json.load(f)
            if filename in all_permissions:
                del all_permissions[filename]
                with open(permissions_file, 'w') as f:
                    json.dump(all_permissions, f, indent=2)
        except:
            pass
            
        # Log action
        from utils.secure_ops import log_secure_action
        log_secure_action(
            current_user['user_id'],
            'file_deleted',
            get_client_ip(request),
            'success',
            f'Moved file to recycle bin: {filename}'
        )
        
        return jsonify(success_response(None, 'File moved to recycle bin'))
    except Exception as e:
        return error_response(f'Failed to delete file: {str(e)}', 500)

@file_manager_bp.route('/upload', methods=['POST'])
@token_required
def upload_file(current_user):
    """Upload a file with optional encryption and permissions"""
    if 'file' not in request.files:
        return error_response('No file part')
    
    file = request.files['file']
    
    if file.filename == '':
        return error_response('No selected file')
    
    if file:
        try:
            from cryptography.fernet import Fernet
            import base64
            import json
            
            filename = secure_filename(file.filename)
            encrypt = request.form.get('encrypt', 'false').lower() == 'true'
            passcode = request.form.get('passcode', '')
            permissions_str = request.form.get('permissions', '{"view": true, "download": true, "edit": false, "delete": false}')
            permissions = json.loads(permissions_str)
            
            # AppLock
            applock = request.form.get('applock', 'false').lower() == 'true'
            applock_passcode = request.form.get('applock_passcode', '')
            
            lock_hash = None
            if applock:
                if not applock_passcode:
                    return error_response('Passcode is required for AppLock')
                lock_hash = generate_password_hash(applock_passcode)
            
            # Read file content as bytes
            content = file.read()
            
            final_filename = filename
            
            # If encryption is requested
            if encrypt:
                if not passcode:
                    return error_response('Passcode is required for encryption')
                
                # Generate encryption key from passcode
                import hashlib
                key = base64.urlsafe_b64encode(hashlib.sha256(passcode.encode()).digest())
                cipher = Fernet(key)
                
                # Encrypt the content
                encrypted_content = cipher.encrypt(content)
                
                # Save encrypted file with .enc extension
                final_filename = filename + '.enc'
                file_path = os.path.join(SANDBOX_DIR, final_filename)
                
                with open(file_path, 'wb') as f:
                    f.write(encrypted_content)
                
                # Log the action
                from utils.secure_ops import log_secure_action
                log_secure_action(
                    current_user['user_id'],
                    'file_upload_encrypted',
                    get_client_ip(request),
                    'success',
                    f'Uploaded and encrypted file: {filename}'
                )
            else:
                # Save file without encryption
                file_path = os.path.join(SANDBOX_DIR, filename)
                
                with open(file_path, 'wb') as f:
                    f.write(content)
                
                # Log the action
                from utils.secure_ops import log_secure_action
                log_secure_action(
                    current_user['user_id'],
                    'file_upload',
                    get_client_ip(request),
                    'success',
                    f'Uploaded file: {filename}'
                )
            
            # Save permissions and lock status
            save_file_permissions(final_filename, permissions, current_user['user_id'], applock, lock_hash)
            
            return jsonify(success_response({
                'filename': final_filename,
                'encrypted': encrypt,
                'permissions': permissions,
                'locked': applock
            }, 'File uploaded successfully'))
                
        except Exception as e:
            return error_response(f'Failed to upload file: {str(e)}', 500)

def save_file_permissions(filename, permissions, user_id, is_locked=False, lock_hash=None):
    """Save file permissions to JSON file"""
    import json
    permissions_file = os.path.join(os.path.dirname(__file__), '..', 'file_permissions.json')
    
    try:
        with open(permissions_file, 'r') as f:
            all_permissions = json.load(f)
    except:
        all_permissions = {}
    
    all_permissions[filename] = {
        'view': permissions.get('view', True),
        'download': permissions.get('download', True),
        'edit': permissions.get('edit', False),
        'delete': permissions.get('delete', False),
        'owner': user_id,
        'is_locked': is_locked,
        'lock_hash': lock_hash
    }
    
    with open(permissions_file, 'w') as f:
        json.dump(all_permissions, f, indent=2)

def get_file_permissions(filename):
    """Get file permissions from JSON file"""
    import json
    permissions_file = os.path.join(os.path.dirname(__file__), '..', 'file_permissions.json')
    
    try:
        with open(permissions_file, 'r') as f:
            all_permissions = json.load(f)
        return all_permissions.get(filename, {
            'view': True,
            'download': True,
            'edit': False,
            'delete': False,
            'owner': None
        })
    except:
        return {
            'view': True,
            'download': True,
            'edit': False,
            'delete': False,
            'owner': None
        }

@file_manager_bp.route('/download/<filename>', methods=['GET'])
@token_required
def download_file(current_user, filename):
    """Download a file"""
    try:
        filename = secure_filename(filename)
        if not is_safe_path(filename):
             return error_response('Invalid filename.')
        
        file_path = os.path.join(SANDBOX_DIR, filename)
        if not os.path.exists(file_path):
            return error_response('File not found.', 404)
        
        # Check download permission (admin bypasses this check)
        if current_user['role'] != 'admin':
            permissions = get_file_permissions(filename)
            if not permissions.get('download', True):
                # Log the failed attempt
                from utils.secure_ops import log_secure_action
                log_secure_action(
                    current_user['user_id'],
                    'file_download_denied',
                    get_client_ip(request),
                    'failure',
                    f'Download denied for file: {filename}'
                )
                return error_response('You do not have permission to download this file.', 403)
        
        # Check File Lock (for admin too, or maybe admin bypasses? Let's enforce for all if locked)
        permissions = get_file_permissions(filename)
        if permissions.get('is_locked', False):
            passcode = request.headers.get('X-File-Passcode')
            if not passcode or not check_password_hash(permissions.get('lock_hash', ''), passcode):
                return error_response('File is locked. Passcode required.', 403, {'locked': True})
        
        # Log successful download
        from utils.secure_ops import log_secure_action
        log_secure_action(
            current_user['user_id'],
            'file_download',
            get_client_ip(request),
            'success',
            f'Downloaded file: {filename}'
        )
            
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return error_response(f'Failed to download file: {str(e)}', 500)

@file_manager_bp.route('/permissions/<filename>', methods=['GET'])
@token_required
def get_permissions_endpoint(current_user, filename):
    '''Get file permissions'''
    try:
        permissions = get_file_permissions(filename)
        return jsonify(success_response(permissions))
    except Exception as e:
        return error_response(f'Failed to get permissions: {str(e)}', 500)

