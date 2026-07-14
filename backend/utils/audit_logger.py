import os
import json
import subprocess
from datetime import datetime
from pathlib import Path

AUDIT_LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
AUDIT_LOG_FILE = os.path.join(AUDIT_LOG_DIR, 'audit.log')


def _ensure_log_directory():
    """Ensure log directory exists"""
    Path(AUDIT_LOG_DIR).mkdir(parents=True, exist_ok=True)


def _set_append_only(file_path):
    """Set append-only flag on log file (Unix-like systems only)"""
    try:
        subprocess.run(['chattr', '+a', file_path], check=False)
    except (FileNotFoundError, OSError):
        pass


def log_audit_event(user_id, action_type, ip_address, status, details):
    """
    Log audit event to file with append-only protection.

    Appends JSON-formatted audit entry to log file. On Unix-like systems,
    the log file is marked append-only to prevent tampering.
    """
    _ensure_log_directory()

    event = {
        'timestamp': datetime.utcnow().isoformat(),
        'user_id': user_id,
        'action_type': action_type,
        'ip_address': ip_address,
        'status': status,
        'details': details
    }

    try:
        with open(AUDIT_LOG_FILE, 'a') as f:
            f.write(json.dumps(event) + '\n')
            f.flush()
            os.fsync(f.fileno())

        _set_append_only(AUDIT_LOG_FILE)
    except Exception as e:
        import logging
        logging.error(f"Failed to write audit log: {e}")


def get_audit_logs(limit=None, offset=0):
    """Read audit logs from file"""
    _ensure_log_directory()

    if not os.path.exists(AUDIT_LOG_FILE):
        return []

    logs = []
    try:
        with open(AUDIT_LOG_FILE, 'r') as f:
            for line in f:
                if line.strip():
                    try:
                        log_entry = json.loads(line.strip())
                        logs.append(log_entry)
                    except json.JSONDecodeError:
                        pass
    except Exception as e:
        import logging
        logging.error(f"Failed to read audit logs: {e}")
        return []

    if offset:
        logs = logs[offset:]
    if limit:
        logs = logs[:limit]

    return logs
