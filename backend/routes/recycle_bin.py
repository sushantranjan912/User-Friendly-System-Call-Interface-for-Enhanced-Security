from flask import Blueprint, request, jsonify
import os
import shutil
import json
import time
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
from utils.auth_utils import token_required
from utils.helpers import success_response, error_response, get_client_ip
from utils.secure_ops import SANDBOX_DIR, log_secure_action
from config import Config

recycle_bin_bp = Blueprint('recycle_bin', __name__)

# Recycle bin directory
RECYCLE_BIN_DIR = os.path.join(os.path.dirname(SANDBOX_DIR), 'recycle_bin')
RECYCLE_METADATA_FILE = os.path.join(RECYCLE_BIN_DIR, 'metadata.json')

# Ensure recycle bin exists
if not os.path.exists(RECYCLE_BIN_DIR):
    os.makedirs(RECYCLE_BIN_DIR)

def get_recycle_metadata():
    """Load recycle bin metadata"""
    if os.path.exists(RECYCLE_METADATA_FILE):
        try:
            with open(RECYCLE_METADATA_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_recycle_metadata(metadata):
    """Save recycle bin metadata"""
    with open(RECYCLE_METADATA_FILE, 'w') as f:
        json.dump(metadata, f, indent=2)

def cleanup_expired_files():
    """Remove files older than 30 minutes"""
    metadata = get_recycle_metadata()
    current_time = time.time()
    expired_files = []
    
    for filename, info in list(metadata.items()):
        delete_time = info.get('deleted_at', 0)
        # 30 minutes = 1800 seconds
        if current_time - delete_time > 1800:
            expired_files.append(filename)
            # Permanently delete
            file_path = os.path.join(RECYCLE_BIN_DIR, filename)
            if os.path.exists(file_path):
                os.remove(file_path)
            # Remove from metadata
            del metadata[filename]
    
    if expired_files:
        save_recycle_metadata(metadata)
    
    return expired_files

@recycle_bin_bp.route('/', methods=['GET'])
@token_required
def list_recycle_bin(current_user):
    """List files in recycle bin"""
    try:
        # Clean up expired files first
        cleanup_expired_files()
        
        metadata = get_recycle_metadata()
        files = []
        current_time = time.time()
        
        for filename, info in metadata.items():
            file_path = os.path.join(RECYCLE_BIN_DIR, filename)
            if os.path.exists(file_path):
                stats = os.stat(file_path)
                deleted_at = info.get('deleted_at', 0)
                time_remaining = max(0, 1800 - (current_time - deleted_at))  # 30 min = 1800 sec
                
                files.append({
                    'name': info.get('original_name', filename),
                    'internal_name': filename,
                    'size': stats.st_size,
                    'deleted_at': deleted_at,
                    'deleted_by': info.get('deleted_by'),
                    'time_remaining': int(time_remaining),
                    'original_permissions': info.get('permissions', {})
                })
        
        # Sort by deletion time (newest first)
        files.sort(key=lambda x: x['deleted_at'], reverse=True)
        
        return jsonify(success_response({'files': files}))
    except Exception as e:
        return error_response(f'Failed to list recycle bin: {str(e)}', 500)

@recycle_bin_bp.route('/restore/<filename>', methods=['POST'])
@token_required
def restore_file(current_user, filename):
    """Restore a file from recycle bin"""
    try:
        metadata = get_recycle_metadata()
        
        if filename not in metadata:
            return error_response('File not found in recycle bin', 404)
        
        info = metadata[filename]
        original_name = info.get('original_name', filename)
        
        recycle_path = os.path.join(RECYCLE_BIN_DIR, filename)
        restore_path = os.path.join(SANDBOX_DIR, original_name)
        
        if not os.path.exists(recycle_path):
            return error_response('File not found in recycle bin', 404)
        
        # Check if file already exists in sandbox
        if os.path.exists(restore_path):
            return error_response(f'File "{original_name}" already exists in sandbox', 400)
        
        # Move file back to sandbox
        shutil.move(recycle_path, restore_path)
        
        # Restore permissions
        if 'permissions' in info:
            permissions_file = os.path.join(os.path.dirname(__file__), '..', 'file_permissions.json')
            try:
                with open(permissions_file, 'r') as f:
                    all_permissions = json.load(f)
            except:
                all_permissions = {}
            
            all_permissions[original_name] = info['permissions']
            
            with open(permissions_file, 'w') as f:
                json.dump(all_permissions, f, indent=2)
        
        # Remove from recycle bin metadata
        del metadata[filename]
        save_recycle_metadata(metadata)
        
        # Log the action
        log_secure_action(
            current_user['user_id'],
            'file_restored',
            get_client_ip(request),
            'success',
            f'Restored file: {original_name}'
        )
        
        return jsonify(success_response(None, f'File "{original_name}" restored successfully'))
    except Exception as e:
        return error_response(f'Failed to restore file: {str(e)}', 500)

@recycle_bin_bp.route('/delete/<filename>', methods=['DELETE'])
@token_required
def permanently_delete(current_user, filename):
    """Permanently delete a file from recycle bin"""
    try:
        metadata = get_recycle_metadata()
        
        if filename not in metadata:
            return error_response('File not found in recycle bin', 404)
        
        info = metadata[filename]
        original_name = info.get('original_name', filename)
        
        recycle_path = os.path.join(RECYCLE_BIN_DIR, filename)
        
        if os.path.exists(recycle_path):
            os.remove(recycle_path)
        
        # Remove from metadata
        del metadata[filename]
        save_recycle_metadata(metadata)
        
        # Log the action
        log_secure_action(
            current_user['user_id'],
            'file_permanently_deleted',
            get_client_ip(request),
            'success',
            f'Permanently deleted file: {original_name}'
        )
        
        return jsonify(success_response(None, f'File "{original_name}" permanently deleted'))
    except Exception as e:
        return error_response(f'Failed to delete file: {str(e)}', 500)

@recycle_bin_bp.route('/empty', methods=['POST'])
@token_required
def empty_recycle_bin(current_user):
    """Empty entire recycle bin"""
    try:
        metadata = get_recycle_metadata()
        deleted_count = 0
        
        for filename in list(metadata.keys()):
            recycle_path = os.path.join(RECYCLE_BIN_DIR, filename)
            if os.path.exists(recycle_path):
                os.remove(recycle_path)
                deleted_count += 1
        
        # Clear metadata
        save_recycle_metadata({})
        
        # Log the action
        log_secure_action(
            current_user['user_id'],
            'recycle_bin_emptied',
            get_client_ip(request),
            'success',
            f'Emptied recycle bin ({deleted_count} files)'
        )
        
        return jsonify(success_response(None, f'Recycle bin emptied ({deleted_count} files deleted)'))
    except Exception as e:
        return error_response(f'Failed to empty recycle bin: {str(e)}', 500)
