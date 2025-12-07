from flask import Flask, send_from_directory, jsonify
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

# Enable CORS for all origins (development mode)
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=False)

# Register blueprints with correct prefixes
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(system_calls_bp, url_prefix='/api/system')
app.register_blueprint(logs_bp, url_prefix='/api')
app.register_blueprint(file_manager_bp, url_prefix='/api/files')
app.register_blueprint(recycle_bin_bp, url_prefix='/api/recycle-bin')

# TEST ENDPOINT
@app.route('/api/test', methods=['GET'])
def test():
    return jsonify({"ok": True, "message": "API is working!", "frontend_dir": FRONTEND_DIR})

# Serve frontend files
@app.route('/')
def index():
    return send_from_directory(FRONTEND_DIR, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    full_path = os.path.join(FRONTEND_DIR, path)
    if os.path.exists(full_path):
        return send_from_directory(FRONTEND_DIR, path)
    # Fallback to index.html for SPA routing
    return send_from_directory(FRONTEND_DIR, 'index.html')

# Error handlers
@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Resource not found', 'success': False}), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({'error': 'Internal server error', 'success': False}), 500

if __name__ == '__main__':
    print(">>> Starting System Call Interface Server...")
    print(f">>> Server running at: http://localhost:5000")
    print(f">>> Security features enabled")
    print(f">>> Allowed commands: {', '.join(Config.ALLOWED_COMMANDS)}")
    print(f">>> Frontend directory: {FRONTEND_DIR}")
    print(f">>> Test endpoint: http://localhost:5000/api/test")
    app.run(debug=True, host='0.0.0.0', port=5000)
