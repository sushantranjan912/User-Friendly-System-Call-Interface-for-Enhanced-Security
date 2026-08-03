from datetime import datetime, timedelta
from database.db_connection import Database
from config import Config

MAX_FAILED_ATTEMPTS = 5
LOCKOUT_DURATION_MINUTES = 15
db = Database(Config.DATABASE_PATH)


def record_login_attempt(ip_address, username, success=False):
    """Record a login attempt in the database"""
    db.execute_insert(
        'INSERT INTO login_attempts (ip_address, username, success) VALUES (?, ?, ?)',
        (ip_address, username, 1 if success else 0)
    )


def get_failed_attempts(ip_address, username, minutes=LOCKOUT_DURATION_MINUTES):
    """Get count of failed login attempts in the last N minutes"""
    cutoff_time = (datetime.utcnow() - timedelta(minutes=minutes)).isoformat()

    attempts = db.execute_query(
        '''SELECT COUNT(*) as count FROM login_attempts
           WHERE ip_address = ? AND username = ? AND success = 0 AND attempt_time > ?''',
        (ip_address, username, cutoff_time)
    )

    return attempts[0]['count'] if attempts else 0


def is_account_locked(ip_address, username):
    """Check if account is locked due to too many failed attempts"""
    failed_count = get_failed_attempts(ip_address, username)
    return failed_count >= MAX_FAILED_ATTEMPTS


def clear_login_attempts(username):
    """Clear login attempts after successful login"""
    db.execute_update(
        'DELETE FROM login_attempts WHERE username = ? AND success = 0',
        (username,)
    )


def get_lockout_remaining_time(ip_address, username):
    """Get remaining lockout time in seconds (returns 0 if not locked)"""
    if not is_account_locked(ip_address, username):
        return 0

    oldest_attempt = db.execute_query(
        '''SELECT attempt_time FROM login_attempts
           WHERE ip_address = ? AND username = ? AND success = 0
           ORDER BY attempt_time ASC LIMIT 1''',
        (ip_address, username)
    )

    if not oldest_attempt:
        return 0

    attempt_time = datetime.fromisoformat(oldest_attempt[0]['attempt_time'])
    lockout_end = attempt_time + timedelta(minutes=LOCKOUT_DURATION_MINUTES)
    remaining = (lockout_end - datetime.utcnow()).total_seconds()

    return max(0, int(remaining))
