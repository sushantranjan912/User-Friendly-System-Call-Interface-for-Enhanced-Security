from flask import Blueprint, request, jsonify
from database.db_connection import Database
from utils.auth_utils import token_required, role_required
from utils.helpers import success_response, error_response
from utils.secure_ops import decrypt_data
from config import Config

logs_bp = Blueprint('logs', __name__)
db = Database(Config.DATABASE_PATH)

@logs_bp.route('/logs', methods=['GET'])
@token_required
def get_logs(current_user):
    """Get audit logs"""
    # Only admins can view all logs, users can only view their own
    limit = request.args.get('limit', 100, type=int)
    offset = request.args.get('offset', 0, type=int)
    action_type = request.args.get('action_type', None)
    
    if current_user['role'] == 'admin':
        # Admin can see all logs
        if action_type:
            logs = db.execute_query(
                '''SELECT l.*, u.username 
                   FROM logs l 
                   LEFT JOIN users u ON l.user_id = u.id 
                   WHERE l.action_type = ?
                   ORDER BY l.created_at DESC 
                   LIMIT ? OFFSET ?''',
                (action_type, limit, offset)
            )
        else:
            logs = db.execute_query(
                '''SELECT l.*, u.username 
                   FROM logs l 
                   LEFT JOIN users u ON l.user_id = u.id 
                   ORDER BY l.created_at DESC 
                   LIMIT ? OFFSET ?''',
                (limit, offset)
            )
    else:
        # Regular users can only see their own logs
        if action_type:
            logs = db.execute_query(
                '''SELECT l.*, u.username 
                   FROM logs l 
                   LEFT JOIN users u ON l.user_id = u.id 
                   WHERE l.user_id = ? AND l.action_type = ?
                   ORDER BY l.created_at DESC 
                   LIMIT ? OFFSET ?''',
                (current_user['user_id'], action_type, limit, offset)
            )
        else:
            logs = db.execute_query(
                '''SELECT l.*, u.username 
                   FROM logs l 
                   LEFT JOIN users u ON l.user_id = u.id 
                   WHERE l.user_id = ?
                   ORDER BY l.created_at DESC 
                   LIMIT ? OFFSET ?''',
                (current_user['user_id'], limit, offset)
            )
    
    logs_list = []
    for row in logs:
        log_dict = dict(row)
        # Decrypt details
        log_dict['details'] = decrypt_data(log_dict.get('details', ''))
        logs_list.append(log_dict)
    
    return jsonify(success_response({
        'logs': logs_list,
        'limit': limit,
        'offset': offset
    }))

@logs_bp.route('/logs/types', methods=['GET'])
@token_required
def get_log_types(current_user):
    """Get available log action types"""
    types = db.execute_query(
        'SELECT DISTINCT action_type FROM logs ORDER BY action_type'
    )
    
    type_list = [row['action_type'] for row in types]
    
    return jsonify(success_response({
        'types': type_list
    }))

@logs_bp.route('/logs/stats', methods=['GET'])
@token_required
@role_required(['admin'])
def get_log_stats(current_user):
    """Get log statistics (admin only)"""
    # Total logs
    total = db.execute_query('SELECT COUNT(*) as count FROM logs')
    
    # Logs by status
    by_status = db.execute_query(
        'SELECT status, COUNT(*) as count FROM logs GROUP BY status'
    )
    
    # Logs by action type
    by_action = db.execute_query(
        'SELECT action_type, COUNT(*) as count FROM logs GROUP BY action_type ORDER BY count DESC LIMIT 10'
    )
    
    # Recent activity (last 24 hours)
    recent = db.execute_query(
        "SELECT COUNT(*) as count FROM logs WHERE created_at >= datetime('now', '-1 day')"
    )
    
    return jsonify(success_response({
        'total_logs': total[0]['count'] if total else 0,
        'by_status': [dict(row) for row in by_status],
        'by_action': [dict(row) for row in by_action],
        'recent_24h': recent[0]['count'] if recent else 0
    }))
