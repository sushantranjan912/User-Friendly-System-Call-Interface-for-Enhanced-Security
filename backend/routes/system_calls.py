from flask import Blueprint, request, jsonify
from database.db_connection import Database
from utils.auth_utils import token_required, role_required
from utils.secure_ops import secure_execute
from utils.helpers import get_client_ip, success_response, error_response
from config import Config

system_calls_bp = Blueprint('system_calls', __name__)
db = Database(Config.DATABASE_PATH)

@system_calls_bp.route('/execute', methods=['POST'])
@token_required
def execute_command(current_user):
    """Execute a system call"""
    data = request.get_json()
    command = data.get('command', '').strip()
    
    if not command:
        return error_response('Command is required.')
    
    try:
        # secure_execute handles whitelisting and logging
        result = secure_execute(command, current_user['user_id'], get_client_ip(request))
        
        # Store in database (legacy table, maybe we should just rely on logs? 
        # But schema has system_calls table. Let's keep it for history view)
        call_id = db.execute_insert(
            'INSERT INTO system_calls (user_id, command, output, status) VALUES (?, ?, ?, ?)',
            (current_user['user_id'], command, result['output'], result['status'])
        )
        
        return jsonify(success_response({
            'call_id': call_id,
            'command': command,
            'output': result['output'],
            'status': result['status'],
            'return_code': result['return_code']
        }, 'Command executed'))
        
    except ValueError as e:
        return error_response(str(e))
    except Exception as e:
        return error_response(f'Execution failed: {str(e)}', 500)

@system_calls_bp.route('/history', methods=['GET'])
@token_required
def get_history(current_user):
    """Get user's command history"""
    limit = request.args.get('limit', 50, type=int)
    offset = request.args.get('offset', 0, type=int)
    
    # Get history
    history = db.execute_query(
        '''SELECT id, command, output, status, executed_at 
           FROM system_calls 
           WHERE user_id = ? 
           ORDER BY executed_at DESC 
           LIMIT ? OFFSET ?''',
        (current_user['user_id'], limit, offset)
    )
    
    history_list = [dict(row) for row in history]
    
    return jsonify(success_response({
        'history': history_list,
        'limit': limit,
        'offset': offset
    }))

@system_calls_bp.route('/allowed-commands', methods=['GET'])
@token_required
def get_allowed_commands(current_user):
    """Get list of allowed commands"""
    return jsonify(success_response({
        'commands': Config.ALLOWED_COMMANDS
    }))

@system_calls_bp.route('/stats', methods=['GET'])
@token_required
def get_stats(current_user):
    """Get user statistics"""
    # Total commands executed
    total = db.execute_query(
        'SELECT COUNT(*) as count FROM system_calls WHERE user_id = ?',
        (current_user['user_id'],)
    )
    
    # Successful commands
    successful = db.execute_query(
        'SELECT COUNT(*) as count FROM system_calls WHERE user_id = ? AND status = ?',
        (current_user['user_id'], 'success')
    )
    
    # Failed commands
    failed = db.execute_query(
        'SELECT COUNT(*) as count FROM system_calls WHERE user_id = ? AND status = ?',
        (current_user['user_id'], 'failure')
    )
    
    # Recent activity (last 24 hours)
    recent = db.execute_query(
        '''SELECT COUNT(*) as count FROM system_calls 
           WHERE user_id = ? AND executed_at >= datetime('now', '-1 day')''',
        (current_user['user_id'],)
    )
    
    return jsonify(success_response({
        'total_commands': total[0]['count'] if total else 0,
        'successful': successful[0]['count'] if successful else 0,
        'failed': failed[0]['count'] if failed else 0,
        'recent_24h': recent[0]['count'] if recent else 0
    }))
