"""
Flask Backend Application for Web Scraper Test Sites
WARNING: Contains intentional security vulnerabilities for SAST workshop training
DO NOT USE IN PRODUCTION!
"""
from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config import config
import os

# Initialize SQLAlchemy
db = SQLAlchemy()


def create_app(config_name='default'):
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    CORS(app, origins=app.config['CORS_ORIGINS'])
    
    # Register blueprints
    from routes.api import api_bp
    from routes.health import health_bp
    from routes.vulnerable_api import vulnerable_bp
    
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(health_bp, url_prefix='/api')
    app.register_blueprint(vulnerable_bp, url_prefix='/api/vulnerable')
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': {
                'code': 'NOT_FOUND',
                'message': 'Resource not found'
            }
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'success': False,
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'Internal server error'
            }
        }), 500
    
    return app


if __name__ == '__main__':
    # Get configuration from environment
    config_name = os.getenv('FLASK_ENV', 'development')
    app = create_app(config_name)
    
    # VULNERABILITY: Running with debug=True (Bandit: B201)
    # This exposes sensitive information and allows code execution
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True  # VULNERABLE: Never use debug=True in production
    )

# Made with Bob
