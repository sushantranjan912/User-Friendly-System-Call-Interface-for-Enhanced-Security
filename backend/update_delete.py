import re

# Read the file
with open('routes/file_manager.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add imports at the top if not present
if 'import shutil' not in content:
    content = content.replace('import os', 'import os\nimport shutil\nimport time\nimport json')

# Find and replace the delete_file function
old_delete_pattern = r'@file_manager_bp\.route\(/\'<filename>\'/,\s*methods=\[/\'DELETE/\'\]\)\s*@token_required\s*def delete_file\(current_user, filename\):.*?(?=\n@|\nclass |\ndef [a-z_]+\(|\nif __name__|$)'

new_delete_function = '''@file_manager_bp.route('/<filename>', methods=['DELETE'])
@token_required
def delete_file(current_user, filename):
    """Move file to recycle bin"""
    try:
        # Check delete permission (admin bypasses this check)
        if current_user['role'] != 'admin':
            permissions = get_file_permissions(filename)
            if not permissions.get('delete', False):
                return error_response('You do not have permission to delete this file.', 403)
        
        filename_safe = secure_filename(filename)
        file_path = os.path.join(SANDBOX_DIR, filename_safe)
        
        if not os.path.exists(file_path):
            return error_response('File not found.', 404)
        
        # Create recycle bin directory
        recycle_bin_dir = os.path.join(os.path.dirname(SANDBOX_DIR), 'recycle_bin')
        if not os.path.exists(recycle_bin_dir):
            os.makedirs(recycle_bin_dir)
        
        # Generate unique name with timestamp
        timestamp = str(int(time.time() * 1000))
        internal_name = f"{timestamp}_{filename_safe}"
        recycle_path = os.path.join(recycle_bin_dir, internal_name)
        
        # Get current permissions
        permissions = get_file_permissions(filename_safe)
        
        # Move file to recycle bin
        shutil.move(file_path, recycle_path)
        
        # Save metadata
        metadata_file = os.path.join(recycle_bin_dir, 'metadata.json')
        try:
            with open(metadata_file, 'r') as f:
                metadata = json.load(f)
        except:
            metadata = {}
        
        metadata[internal_name] = {
            'original_name': filename_safe,
            'deleted_at': time.time(),
            'deleted_by': current_user['user_id'],
            'permissions': permissions
        }
        
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        # Remove from main permissions file
        permissions_file = os.path.join(os.path.dirname(__file__), '..', 'file_permissions.json')
        try:
            with open(permissions_file, 'r') as f:
                all_permissions = json.load(f)
            if filename_safe in all_permissions:
                del all_permissions[filename_safe]
            with open(permissions_file, 'w') as f:
                json.dump(all_permissions, f, indent=2)
        except:
            pass
        
        # Log the action
        from utils.secure_ops import log_secure_action
        log_secure_action(
            current_user['user_id'],
            'file_moved_to_recycle',
            get_client_ip(request),
            'success',
            f'Moved file to recycle bin: {filename_safe}'
        )
        
        return jsonify(success_response(None, 'File moved to recycle bin'))
    except FileNotFoundError:
        return error_response('File not found.', 404)
    except Exception as e:
        return error_response(f'Failed to move file to recycle bin: {str(e)}', 500)

'''

content_modified = re.sub(old_delete_pattern, new_delete_function, content, flags=re.DOTALL)

# Write back
with open('routes/file_manager.py', 'w', encoding='utf-8') as f:
    f.write(content_modified)

print("Updated file_manager.py with recycle bin support")
