import secrets
from database.db_connection import Database
from config import Config

db = Database(Config.DATABASE_PATH)


def generate_session_id():
    """Generate a cryptographically secure session ID"""
    return secrets.token_urlsafe(32)


def create_session(user_id, ip_address):
    """Create a new session for user, invalidating any previous sessions"""
    session_id = generate_session_id()

    db.execute_update(
        'UPDATE users SET session_id = ? WHERE id = ?',
        (session_id, user_id)
    )

    return session_id


def validate_session(user_id, session_id):
    """Validate that the session ID matches the user's current session"""
    result = db.execute_query(
        'SELECT session_id FROM users WHERE id = ? LIMIT 1',
        (user_id,)
    )

    if not result:
        return False

    return result[0]['session_id'] == session_id


def invalidate_session(user_id):
    """Invalidate user's session"""
    db.execute_update(
        'UPDATE users SET session_id = NULL WHERE id = ?',
        (user_id,)
    )
