"""
Flask Application Configuration
WARNING: Contains intentional security vulnerabilities for SAST workshop training
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration"""
    # VULNERABILITY: Hardcoded secret key (Bandit: B105)
    SECRET_KEY = 'super-secret-key-12345-do-not-use-in-production'
    
    # VULNERABILITY: Hardcoded database credentials (Bandit: B105)
    DATABASE_PASSWORD = 'admin123'
    API_KEY = 'sk-1234567890abcdef'
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///data/webscraper.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # CORS configuration
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:8000').split(',')
    
    # Application settings
    JSON_SORT_KEYS = False
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max request size


class DevelopmentConfig(Config):
    """Development configuration"""
    # VULNERABILITY: Debug mode enabled (Bandit: B201)
    DEBUG = True
    TESTING = False
    
    # VULNERABILITY: Hardcoded connection string with credentials (Bandit: B105)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data/webscraper.db'


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    
    # Use environment variables in production
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

# Made with Bob
