"""API routes package"""
from routes.api import api_bp
from routes.health import health_bp
from routes.vulnerable_api import vulnerable_bp

__all__ = ['api_bp', 'health_bp', 'vulnerable_bp']

# Made with Bob
