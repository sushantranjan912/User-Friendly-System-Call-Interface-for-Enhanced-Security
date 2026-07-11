from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS
from config import Config
from routes.auth import auth_bp
from routes.system_calls import system_calls_bp
from routes.logs import logs_bp
from routes.file_manager import file_manager_bp
from routes.recycle_bin import recycle_bin_bp
import os

# Get absolute paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(os.path.dirname(BASE_DIR), 'frontend')

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path='')
app.config.from_object(Config)

# =========================
# SECURITY CONFIGURATION
# =========================

# Enable CORS
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=False)

# Limit request size (5MB)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024


# =========================
# GLOBAL VALIDATION MIDDLEWARE
# =========================
@app.before_request
def validate_requests():

    # Allow frontend + static files
    if not request.path.startswith("/api"):
        return

    # Allow test route
    if request.path == "/api/test":
        return

    # Block empty POST/PUT/DELETE requests
    if request.method in ["POST", "PUT", "DELETE"]:
        if not request.data:
            return jsonify({"error": "Empty request body not allowed"}), 400

    # Validate JSON requests
    if request.is_json:
        data = request.get_json(silent=True)

        if data is None:
            return jsonify({"error": "Invalid JSON format"}), 400

        if isinstance(data, dict) and len(data) == 0:
            return jsonify({"error": "Empty JSON payload not allowed"}), 400


# =========================
# REGISTER BLUEPRINTS
# =========================
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(system_calls_bp, url_prefix='/api/system')
app.register_blueprint(logs_bp, url_prefix='/api')
app.register_blueprint(file_manager_bp, url_prefix='/api/files')
app.register_blueprint(recycle_bin_bp, url_prefix='/api/recycle-bin')


# =========================
# TEST ENDPOINT
# =========================
@app.route('/api/test', methods=['GET'])
def test():
    return jsonify({
        "ok": True,
        "message": "API is working!",
        "frontend_dir": FRONTEND_DIR
    })


# =========================
# SERVE FRONTEND
# =========================
@app.route('/')
def index():
    return send_from_directory(FRONTEND_DIR, 'index.html')


@app.route('/<path:path>')
def serve_static(path):
    full_path = os.path.join(FRONTEND_DIR, path)
    if os.path.exists(full_path):
        return send_from_directory(FRONTEND_DIR, path)
    return send_from_directory(FRONTEND_DIR, 'index.html')


# =========================
# ERROR HANDLERS
# =========================
import logging
import traceback

logger = logging.getLogger(__name__)

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Resource not found', 'success': False}), 404


@app.errorhandler(500)
def internal_error(e):
    return jsonify({'error': 'Internal server error', 'success': False}), 500


@app.errorhandler(Exception)
def handle_exception(e):
    """Catch all unhandled exceptions, log them internally, and return generic error"""
    logger.error("Unhandled exception: %s", traceback.format_exc())
    return jsonify({'error': 'An internal error occurred', 'success': False}), 500


# =========================
# RUN SERVER
# =========================
if __name__ == '__main__':
    print(">>> Starting System Call Interface Server...")
    print(f">>> Server running at: http://localhost:5000")
    print(f">>> Security features enabled")
    print(f">>> Allowed commands: {', '.join(Config.ALLOWED_COMMANDS)}")
    print(f">>> Frontend directory: {FRONTEND_DIR}")
    print(f">>> Test endpoint: http://localhost:5000/api/test")

    debug_mode = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)