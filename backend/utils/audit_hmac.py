import hmac
import hashlib
import json


def generate_audit_mac(secret_key, log_data):
    """Generate HMAC for audit log entry to ensure integrity.

    Args:
        secret_key: Secret key for HMAC generation
        log_data: Dictionary containing audit log fields (user_id, action_type, ip_address, status, details)

    Returns:
        Hex-encoded HMAC digest
    """
    payload = json.dumps(log_data, sort_keys=True, separators=(',', ':'))
    mac = hmac.new(
        secret_key.encode('utf-8'),
        payload.encode('utf-8'),
        hashlib.sha256
    )
    return mac.hexdigest()


def verify_audit_mac(secret_key, log_data, mac_value):
    """Verify HMAC for audit log entry.

    Args:
        secret_key: Secret key for HMAC verification
        log_data: Dictionary containing audit log fields (user_id, action_type, ip_address, status, details)
        mac_value: HMAC value to verify against

    Returns:
        True if MAC is valid, False otherwise
    """
    expected_mac = generate_audit_mac(secret_key, log_data)
    return hmac.compare_digest(expected_mac, mac_value)
