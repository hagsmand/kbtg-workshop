#!/usr/bin/env python3
"""
Quick start script for Flask backend
Handles environment setup and runs the application
"""
import os
import sys
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import flask
        import flask_cors
        import flask_sqlalchemy
        import marshmallow
        print("✓ All dependencies installed")
        return True
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        print("\nPlease install dependencies:")
        print("  pip install -r requirements.txt")
        return False

def setup_environment():
    """Setup environment variables if .env doesn't exist"""
    env_file = Path('.env')
    env_example = Path('.env.example')
    
    if not env_file.exists() and env_example.exists():
        print("Creating .env file from .env.example...")
        env_file.write_text(env_example.read_text())
        print("✓ .env file created")
    elif env_file.exists():
        print("✓ .env file exists")
    else:
        print("⚠ No .env or .env.example file found")

def create_data_directory():
    """Create data directory if it doesn't exist"""
    data_dir = Path('data')
    if not data_dir.exists():
        data_dir.mkdir()
        print("✓ Created data directory")
    else:
        print("✓ Data directory exists")

def main():
    """Main entry point"""
    print("=" * 60)
    print("Flask Backend - Web Scraper Test Sites")
    print("⚠️  WARNING: Contains intentional security vulnerabilities")
    print("=" * 60)
    print()
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Setup environment
    setup_environment()
    
    # Create data directory
    create_data_directory()
    
    print()
    print("Starting Flask application...")
    print("Server will be available at: http://localhost:5000")
    print()
    print("API Endpoints:")
    print("  - GET  /api/test-sites")
    print("  - POST /api/contact")
    print("  - POST /api/feedback")
    print("  - GET  /api/health")
    print("  - GET  /api/vulnerable/info (⚠️  Training only)")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    print()
    
    # Import and run the app
    from app import create_app
    app = create_app('development')
    app.run(host='0.0.0.0', port=5000, debug=True)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nServer stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)

# Made with Bob
