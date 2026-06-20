"""Response formatting utilities"""
from flask import jsonify
from datetime import datetime


def success_response(data=None, message=None, count=None, status_code=200):
    """
    Format success response
    
    Args:
        data: Response data
        message: Success message
        count: Number of items (for lists)
        status_code: HTTP status code
    
    Returns:
        JSON response tuple
    """
    response = {
        'success': True,
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    }
    
    if data is not None:
        response['data'] = data
    if message:
        response['message'] = message
    if count is not None:
        response['count'] = count
    
    return jsonify(response), status_code


def error_response(code, message, status_code=400, details=None):
    """
    Format error response
    
    Args:
        code: Error code
        message: Error message
        status_code: HTTP status code
        details: Additional error details
    
    Returns:
        JSON response tuple
    """
    response = {
        'success': False,
        'error': {
            'code': code,
            'message': message
        }
    }
    
    if details:
        response['error']['details'] = details
    
    return jsonify(response), status_code

# Made with Bob
