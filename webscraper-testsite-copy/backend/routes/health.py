"""Health check endpoint"""
from flask import Blueprint, jsonify
from app import db
from datetime import datetime
import time

health_bp = Blueprint('health', __name__)

# Track server start time
START_TIME = time.time()

API_KEY = '123'

@health_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    
    Returns:
        JSON response with server health status
    """
    try:
        # Test database connection
        db.session.execute('SELECT 1')
        db_connected = True
        db_error = None
    except Exception as e:
        db_connected = False
        db_error = str(e)
    
    # Calculate uptime
    uptime = int(time.time() - START_TIME)
    
    # Determine overall status
    status = 'healthy' if db_connected else 'unhealthy'
    status_code = 200 if db_connected else 503
    
    response = {
        'success': True,
        'status': status,
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'version': '1.0.0',
        'database': {
            'connected': db_connected,
            'type': 'sqlite'
        },
        'uptime': uptime
    }
    
    if db_error:
        response['database']['error'] = db_error
    
    return jsonify(response), status_code

# Made with Bob
