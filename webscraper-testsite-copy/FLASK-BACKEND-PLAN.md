# Flask Backend Implementation Plan
## Web Scraper Test Sites API

**Version**: 1.0  
**Date**: June 20, 2026  
**Status**: Planning Phase

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Project Structure](#project-structure)
4. [API Endpoints](#api-endpoints)
5. [Database Schema](#database-schema)
6. [Technology Stack](#technology-stack)
7. [Implementation Steps](#implementation-steps)
8. [Frontend Integration](#frontend-integration)
9. [Testing Strategy](#testing-strategy)
10. [Deployment](#deployment)
11. [⚠️ Security Workshop - Vulnerable Code Examples](#security-workshop)

---

## ⚠️ WORKSHOP NOTICE

**This implementation includes intentional security vulnerabilities for SAST (Static Application Security Testing) training purposes.**

These vulnerabilities are designed to be detected by security scanning tools like:
- Bandit (Python)
- SonarQube
- Snyk
- Semgrep
- GitHub Advanced Security

**DO NOT use these vulnerable code examples in production!**

---

## 🎯 Overview

### Purpose
Create a Flask REST API backend to serve dynamic content and handle user interactions for the Web Scraper Test Sites application.

### Goals
- ✅ Serve test site data dynamically via API
- ✅ Handle contact form submissions
- ✅ Collect and store user feedback
- ✅ Provide clean, RESTful API design
- ✅ Implement proper validation and error handling
- ✅ Enable CORS for frontend communication
- ✅ Use SQLite for data persistence

### Current State
- Static HTML/CSS/JavaScript website
- Running on Python HTTP server (port 8000)
- No backend functionality
- No data persistence

### Target State
- Flask API backend (port 5000)
- Frontend consuming API endpoints
- Database for storing contacts and feedback
- Validated and sanitized user inputs
- Comprehensive error handling

---

## 🏗️ Architecture

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Client Browser                        │
│                    (localhost:8000)                          │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ HTTP Requests (CORS enabled)
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                     Flask API Server                         │
│                    (localhost:5000)                          │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Routes Layer                                         │  │
│  │  - /api/test-sites (GET)                            │  │
│  │  - /api/contact (POST)                              │  │
│  │  - /api/feedback (POST)                             │  │
│  │  - /api/health (GET)                                │  │
│  └────────────────┬─────────────────────────────────────┘  │
│                   │                                          │
│  ┌────────────────▼─────────────────────────────────────┐  │
│  │  Business Logic Layer                                 │  │
│  │  - Input Validation (Marshmallow)                    │  │
│  │  - Data Processing                                   │  │
│  │  - Error Handling                                    │  │
│  └────────────────┬─────────────────────────────────────┘  │
│                   │                                          │
│  ┌────────────────▼─────────────────────────────────────┐  │
│  │  Data Access Layer                                    │  │
│  │  - SQLAlchemy ORM                                    │  │
│  │  - Models (Contact, Feedback)                        │  │
│  └────────────────┬─────────────────────────────────────┘  │
└───────────────────┼──────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────┐
│                    SQLite Database                           │
│                  (webscraper.db)                             │
│  - contacts table                                            │
│  - feedback table                                            │
└─────────────────────────────────────────────────────────────┘
```

### Design Patterns

1. **MVC Pattern**: Separation of concerns
   - Models: Database entities
   - Views: API endpoints (routes)
   - Controllers: Business logic

2. **Repository Pattern**: Data access abstraction
   - Models handle database operations
   - Routes handle HTTP logic

3. **Factory Pattern**: Application creation
   - `create_app()` function for Flask app initialization

---

## 📁 Project Structure

```
webscraper-testsite-copy/
├── backend/                          # Backend directory
│   ├── app.py                       # Main Flask application entry point
│   ├── config.py                    # Configuration settings
│   ├── requirements.txt             # Python dependencies
│   ├── .env                         # Environment variables (not in git)
│   ├── .env.example                 # Example environment file
│   │
│   ├── routes/                      # API route handlers
│   │   ├── __init__.py
│   │   ├── api.py                  # Main API endpoints
│   │   └── health.py               # Health check endpoint
│   │
│   ├── models/                      # Database models
│   │   ├── __init__.py
│   │   ├── database.py             # Database initialization
│   │   ├── contact.py              # Contact model
│   │   └── feedback.py             # Feedback model
│   │
│   ├── schemas/                     # Validation schemas
│   │   ├── __init__.py
│   │   ├── test_site.py            # Test site schema
│   │   ├── contact.py              # Contact validation
│   │   └── feedback.py             # Feedback validation
│   │
│   ├── utils/                       # Utility functions
│   │   ├── __init__.py
│   │   ├── validators.py           # Custom validators
│   │   ├── responses.py            # Response formatters
│   │   └── errors.py               # Error handlers
│   │
│   ├── data/                        # Data files
│   │   ├── test_sites.json         # Test sites data
│   │   └── webscraper.db           # SQLite database (generated)
│   │
│   └── tests/                       # Test files
│       ├── __init__.py
│       ├── test_api.py             # API endpoint tests
│       ├── test_models.py          # Model tests
│       └── test_validators.py      # Validation tests
│
├── index.html                       # Frontend HTML
├── css/                             # Frontend styles
├── js/                              # Frontend JavaScript
├── images/                          # Images
│
├── API-DOCUMENTATION.md             # API documentation
├── FLASK-BACKEND-PLAN.md           # This file
└── README.md                        # Project README
```

---

## 🔌 API Endpoints

### Base URL
```
http://localhost:5000/api
```

### Endpoint Summary

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/test-sites` | Get all test sites | No |
| GET | `/api/test-sites/:id` | Get single test site | No |
| POST | `/api/contact` | Submit contact form | No |
| POST | `/api/feedback` | Submit feedback | No |
| GET | `/api/health` | Health check | No |

---

### 1. GET /api/test-sites

**Description**: Retrieve all test site cards

**Request**:
```http
GET /api/test-sites HTTP/1.1
Host: localhost:5000
```

**Response** (200 OK):
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "title": "E-commerce site",
      "description": "E-commerce site with multiple categories, subcategories. All items are loaded in one page.",
      "image": "images/ecommerce-allinone.png",
      "url": "#",
      "category": "ecommerce",
      "difficulty": "beginner"
    },
    {
      "id": 2,
      "title": "E-commerce site with pagination links",
      "description": "E-commerce site with multiple categories, subcategories. Standard links are used for pagination.",
      "image": "images/ecommerce-static.png",
      "url": "#",
      "category": "ecommerce",
      "difficulty": "intermediate"
    }
  ],
  "count": 6,
  "timestamp": "2026-06-20T11:00:00Z"
}
```

**Error Response** (500):
```json
{
  "success": false,
  "error": {
    "code": "INTERNAL_ERROR",
    "message": "Failed to retrieve test sites"
  }
}
```

---

### 2. GET /api/test-sites/:id

**Description**: Retrieve a single test site by ID

**Request**:
```http
GET /api/test-sites/1 HTTP/1.1
Host: localhost:5000
```

**Response** (200 OK):
```json
{
  "success": true,
  "data": {
    "id": 1,
    "title": "E-commerce site",
    "description": "E-commerce site with multiple categories, subcategories. All items are loaded in one page.",
    "image": "images/ecommerce-allinone.png",
    "url": "#",
    "category": "ecommerce",
    "difficulty": "beginner",
    "features": [
      "Multiple categories",
      "Subcategories",
      "All items in one page"
    ]
  }
}
```

**Error Response** (404):
```json
{
  "success": false,
  "error": {
    "code": "NOT_FOUND",
    "message": "Test site with ID 1 not found"
  }
}
```

---

### 3. POST /api/contact

**Description**: Submit a contact form

**Request**:
```http
POST /api/contact HTTP/1.1
Host: localhost:5000
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john.doe@example.com",
  "subject": "Question about web scraping",
  "message": "I have a question about how to scrape dynamic content..."
}
```

**Validation Rules**:
- `name`: Required, 2-100 characters, alphanumeric with spaces
- `email`: Required, valid email format, max 255 characters
- `subject`: Required, 5-200 characters
- `message`: Required, 10-2000 characters

**Response** (201 Created):
```json
{
  "success": true,
  "data": {
    "id": 123,
    "name": "John Doe",
    "email": "john.doe@example.com",
    "subject": "Question about web scraping",
    "status": "new",
    "created_at": "2026-06-20T11:00:00Z"
  },
  "message": "Contact form submitted successfully. We'll get back to you soon!"
}
```

**Error Response** (400 Bad Request):
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed",
    "details": {
      "email": ["Not a valid email address"],
      "message": ["Field must be at least 10 characters long"]
    }
  }
}
```

**Error Response** (429 Too Many Requests):
```json
{
  "success": false,
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Too many requests. Please try again later.",
    "retry_after": 60
  }
}
```

---

### 4. POST /api/feedback

**Description**: Submit user feedback

**Request**:
```http
POST /api/feedback HTTP/1.1
Host: localhost:5000
Content-Type: application/json

{
  "rating": 5,
  "comment": "Great tool! Very helpful for learning web scraping.",
  "page": "test-sites",
  "email": "user@example.com"
}
```

**Validation Rules**:
- `rating`: Required, integer 1-5
- `comment`: Required, 5-1000 characters
- `page`: Optional, max 100 characters
- `email`: Optional, valid email format if provided

**Response** (201 Created):
```json
{
  "success": true,
  "data": {
    "id": 456,
    "rating": 5,
    "page": "test-sites",
    "created_at": "2026-06-20T11:00:00Z"
  },
  "message": "Thank you for your feedback!"
}
```

**Error Response** (400 Bad Request):
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed",
    "details": {
      "rating": ["Must be between 1 and 5"],
      "comment": ["Field is required"]
    }
  }
}
```

---

### 5. GET /api/health

**Description**: Health check endpoint

**Request**:
```http
GET /api/health HTTP/1.1
Host: localhost:5000
```

**Response** (200 OK):
```json
{
  "success": true,
  "status": "healthy",
  "timestamp": "2026-06-20T11:00:00Z",
  "version": "1.0.0",
  "database": {
    "connected": true,
    "type": "sqlite"
  },
  "uptime": 3600
}
```

**Error Response** (503 Service Unavailable):
```json
{
  "success": false,
  "status": "unhealthy",
  "error": {
    "code": "DATABASE_ERROR",
    "message": "Database connection failed"
  }
}
```

---

## 🗄️ Database Schema

### Database: SQLite (webscraper.db)

### Table: contacts

```sql
CREATE TABLE contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL,
    subject VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'new',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Indexes for performance
    INDEX idx_email (email),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at)
);
```

**Fields**:
- `id`: Auto-incrementing primary key
- `name`: Contact person's name
- `email`: Contact email address
- `subject`: Message subject
- `message`: Full message content
- `status`: Status (new, read, replied, archived)
- `created_at`: Timestamp when created
- `updated_at`: Timestamp when last updated

**Sample Data**:
```sql
INSERT INTO contacts (name, email, subject, message) VALUES
('John Doe', 'john@example.com', 'Question', 'How do I scrape AJAX content?'),
('Jane Smith', 'jane@example.com', 'Feedback', 'Great tool!');
```

---

### Table: feedback

```sql
CREATE TABLE feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rating INTEGER NOT NULL CHECK(rating >= 1 AND rating <= 5),
    comment TEXT NOT NULL,
    page VARCHAR(100),
    email VARCHAR(255),
    user_agent TEXT,
    ip_address VARCHAR(45),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Indexes for performance
    INDEX idx_rating (rating),
    INDEX idx_page (page),
    INDEX idx_created_at (created_at)
);
```

**Fields**:
- `id`: Auto-incrementing primary key
- `rating`: Rating from 1 to 5
- `comment`: Feedback comment
- `page`: Page where feedback was submitted
- `email`: Optional user email
- `user_agent`: Browser user agent (auto-captured)
- `ip_address`: User IP address (auto-captured)
- `created_at`: Timestamp when created

**Sample Data**:
```sql
INSERT INTO feedback (rating, comment, page, email) VALUES
(5, 'Excellent tool!', 'test-sites', 'user1@example.com'),
(4, 'Very helpful', 'test-sites', NULL);
```

---

### Database Relationships

```
┌─────────────────┐
│    contacts     │
│─────────────────│
│ id (PK)         │
│ name            │
│ email           │
│ subject         │
│ message         │
│ status          │
│ created_at      │
│ updated_at      │
└─────────────────┘

┌─────────────────┐
│    feedback     │
│─────────────────│
│ id (PK)         │
│ rating          │
│ comment         │
│ page            │
│ email           │
│ user_agent      │
│ ip_address      │
│ created_at      │
└─────────────────┘
```

*Note: No foreign key relationships in current design. Tables are independent.*

---

## 🛠️ Technology Stack

### Backend Framework
- **Flask 3.0+**: Lightweight Python web framework
- **Flask-CORS**: Cross-Origin Resource Sharing support
- **Flask-SQLAlchemy**: ORM for database operations
- **Flask-Migrate**: Database migrations (optional)

### Validation & Serialization
- **Marshmallow 3.x**: Object serialization and validation
- **marshmallow-sqlalchemy**: SQLAlchemy integration

### Database
- **SQLite**: Lightweight file-based database
- **SQLAlchemy**: Python SQL toolkit and ORM

### Configuration
- **python-dotenv**: Environment variable management

### Development Tools
- **pytest**: Testing framework
- **pytest-flask**: Flask testing utilities
- **black**: Code formatter
- **flake8**: Linting tool

### Optional Enhancements
- **Flask-Limiter**: Rate limiting
- **Flask-Caching**: Response caching
- **gunicorn**: Production WSGI server

---

## 📝 Implementation Steps

### Phase 1: Project Setup (30 minutes)

#### Step 1.1: Create Backend Directory Structure
```bash
cd webscraper-testsite-copy
mkdir backend
cd backend
mkdir routes models schemas utils data tests
touch app.py config.py requirements.txt .env.example
```

#### Step 1.2: Create requirements.txt
```txt
Flask==3.0.0
Flask-CORS==4.0.0
Flask-SQLAlchemy==3.1.1
marshmallow==3.20.1
marshmallow-sqlalchemy==0.30.0
python-dotenv==1.0.0
pytest==7.4.3
pytest-flask==1.3.0
```

#### Step 1.3: Create .env.example
```env
FLASK_APP=app.py
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///data/webscraper.db
CORS_ORIGINS=http://localhost:8000
```

#### Step 1.4: Install Dependencies
```bash
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

---

### Phase 2: Core Application Setup (45 minutes)

#### Step 2.1: Create config.py
```python
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///data/webscraper.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:8000').split(',')

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
```

#### Step 2.2: Create app.py
```python
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    CORS(app, origins=app.config['CORS_ORIGINS'])
    
    # Register blueprints
    from routes.api import api_bp
    from routes.health import health_bp
    
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(health_bp, url_prefix='/api')
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000)
```

---

### Phase 3: Database Models (30 minutes)

#### Step 3.1: Create models/database.py
```python
from app import db
from datetime import datetime

class TimestampMixin:
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

#### Step 3.2: Create models/contact.py
```python
from app import db
from models.database import TimestampMixin

class Contact(db.Model, TimestampMixin):
    __tablename__ = 'contacts'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), nullable=False, index=True)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='new', index=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'subject': self.subject,
            'status': self.status,
            'created_at': self.created_at.isoformat()
        }
```

#### Step 3.3: Create models/feedback.py
```python
from app import db
from datetime import datetime

class Feedback(db.Model):
    __tablename__ = 'feedback'
    
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=False)
    page = db.Column(db.String(100))
    email = db.Column(db.String(255))
    user_agent = db.Column(db.Text)
    ip_address = db.Column(db.String(45))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'rating': self.rating,
            'page': self.page,
            'created_at': self.created_at.isoformat()
        }
```

---

### Phase 4: Validation Schemas (30 minutes)

#### Step 4.1: Create schemas/contact.py
```python
from marshmallow import Schema, fields, validate, ValidationError

class ContactSchema(Schema):
    name = fields.Str(
        required=True,
        validate=[
            validate.Length(min=2, max=100),
            validate.Regexp(r'^[a-zA-Z\s]+$', error='Name must contain only letters and spaces')
        ]
    )
    email = fields.Email(required=True, validate=validate.Length(max=255))
    subject = fields.Str(required=True, validate=validate.Length(min=5, max=200))
    message = fields.Str(required=True, validate=validate.Length(min=10, max=2000))
```

#### Step 4.2: Create schemas/feedback.py
```python
from marshmallow import Schema, fields, validate

class FeedbackSchema(Schema):
    rating = fields.Int(
        required=True,
        validate=validate.Range(min=1, max=5, error='Rating must be between 1 and 5')
    )
    comment = fields.Str(required=True, validate=validate.Length(min=5, max=1000))
    page = fields.Str(validate=validate.Length(max=100))
    email = fields.Email(validate=validate.Length(max=255))
```

---

### Phase 5: API Routes (60 minutes)

#### Step 5.1: Create routes/api.py
```python
from flask import Blueprint, request, jsonify
from app import db
from models.contact import Contact
from models.feedback import Feedback
from schemas.contact import ContactSchema
from schemas.feedback import FeedbackSchema
from utils.responses import success_response, error_response
from marshmallow import ValidationError
import json

api_bp = Blueprint('api', __name__)

# Load test sites data
with open('data/test_sites.json', 'r') as f:
    TEST_SITES = json.load(f)

@api_bp.route('/test-sites', methods=['GET'])
def get_test_sites():
    """Get all test sites"""
    return success_response(
        data=TEST_SITES,
        count=len(TEST_SITES)
    )

@api_bp.route('/test-sites/<int:site_id>', methods=['GET'])
def get_test_site(site_id):
    """Get single test site by ID"""
    site = next((s for s in TEST_SITES if s['id'] == site_id), None)
    if not site:
        return error_response('NOT_FOUND', f'Test site with ID {site_id} not found', 404)
    return success_response(data=site)

@api_bp.route('/contact', methods=['POST'])
def submit_contact():
    """Submit contact form"""
    schema = ContactSchema()
    try:
        data = schema.load(request.json)
        contact = Contact(**data)
        db.session.add(contact)
        db.session.commit()
        
        return success_response(
            data=contact.to_dict(),
            message="Contact form submitted successfully. We'll get back to you soon!",
            status_code=201
        )
    except ValidationError as e:
        return error_response('VALIDATION_ERROR', 'Validation failed', 400, e.messages)

@api_bp.route('/feedback', methods=['POST'])
def submit_feedback():
    """Submit feedback"""
    schema = FeedbackSchema()
    try:
        data = schema.load(request.json)
        feedback = Feedback(
            **data,
            user_agent=request.headers.get('User-Agent'),
            ip_address=request.remote_addr
        )
        db.session.add(feedback)
        db.session.commit()
        
        return success_response(
            data=feedback.to_dict(),
            message="Thank you for your feedback!",
            status_code=201
        )
    except ValidationError as e:
        return error_response('VALIDATION_ERROR', 'Validation failed', 400, e.messages)
```

#### Step 5.2: Create routes/health.py
```python
from flask import Blueprint, jsonify
from app import db
from datetime import datetime
import time

health_bp = Blueprint('health', __name__)
start_time = time.time()

@health_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        # Test database connection
        db.session.execute('SELECT 1')
        db_connected = True
    except Exception:
        db_connected = False
    
    uptime = int(time.time() - start_time)
    
    return jsonify({
        'success': True,
        'status': 'healthy' if db_connected else 'unhealthy',
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'version': '1.0.0',
        'database': {
            'connected': db_connected,
            'type': 'sqlite'
        },
        'uptime': uptime
    }), 200 if db_connected else 503
```

---

### Phase 6: Utilities (20 minutes)

#### Step 6.1: Create utils/responses.py
```python
from flask import jsonify
from datetime import datetime

def success_response(data=None, message=None, count=None, status_code=200):
    """Format success response"""
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
    """Format error response"""
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
```

---

### Phase 7: Test Data (15 minutes)

#### Step 7.1: Create data/test_sites.json
```json
[
  {
    "id": 1,
    "title": "E-commerce site",
    "description": "E-commerce site with multiple categories, subcategories. All items are loaded in one page.",
    "image": "images/ecommerce-allinone.png",
    "url": "#",
    "category": "ecommerce",
    "difficulty": "beginner"
  },
  {
    "id": 2,
    "title": "E-commerce site with pagination links",
    "description": "E-commerce site with multiple categories, subcategories. Standard links are used for pagination.",
    "image": "images/ecommerce-static.png",
    "url": "#",
    "category": "ecommerce",
    "difficulty": "intermediate"
  },
  {
    "id": 3,
    "title": "E-commerce site with AJAX pagination links",
    "description": "E-commerce site with multiple categories, subcategories. Dynamic links that use data without reloading the page for pagination.",
    "image": "images/ecommerce-ajax.png",
    "url": "#",
    "category": "ecommerce",
    "difficulty": "advanced"
  },
  {
    "id": 4,
    "title": "E-commerce site with Load more buttons",
    "description": "E-commerce site with multiple categories, subcategories. Instead of using pagination this site uses a Load more button to load more items.",
    "image": "images/ecommerce-more.png",
    "url": "#",
    "category": "ecommerce",
    "difficulty": "intermediate"
  },
  {
    "id": 5,
    "title": "E-commerce site that loads items while scrolling",
    "description": "E-commerce site with multiple categories, subcategories. Instead of using pagination this site loads items when user scrolls the page down.",
    "image": "images/ecommerce-scroll.png",
    "url": "#",
    "category": "ecommerce",
    "difficulty": "advanced"
  },
  {
    "id": 6,
    "title": "Table playground",
    "description": "This page contains multiple tables. You can train using Table selector here.",
    "image": "images/tables.png",
    "url": "#",
    "category": "tables",
    "difficulty": "beginner"
  }
]
```

---

## 🔗 Frontend Integration

### Update js/main.js

Add API integration functions:

```javascript
// API Configuration
const API_BASE_URL = 'http://localhost:5000/api';

// Fetch test sites from API
async function fetchTestSites() {
    try {
        const response = await fetch(`${API_BASE_URL}/test-sites`);
        const result = await response.json();
        
        if (result.success) {
            renderTestSites(result.data);
        } else {
            console.error('Failed to fetch test sites:', result.error);
        }
    } catch (error) {
        console.error('Error fetching test sites:', error);
    }
}

// Render test sites dynamically
function renderTestSites(sites) {
    const container = document.querySelector('.test-sites');
    container.innerHTML = sites.map((site, index) => `
        <article class="test-site-card">
            <div class="card-content">
                <h2 class="card-title">
                    <a href="${site.url}">${site.title}</a>
                </h2>
                <p class="card-description">${site.description}</p>
            </div>
            <div class="card-image">
                <img src="${site.image}" alt="${site.title}">
            </div>
        </article>
        ${index < sites.length - 1 ? '<hr class="divider">' : ''}
    `).join('');
}

// Submit contact form
async function submitContactForm(formData) {
    try {
        const response = await fetch(`${API_BASE_URL}/contact`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        const result = await response.json();
        
        if (result.success) {
            alert(result.message);
            return true;
        } else {
            alert('Error: ' + result.error.message);
            return false;
        }
    } catch (error) {
        console.error('Error submitting contact form:', error);
        alert('Failed to submit form. Please try again.');
        return false;
    }
}

// Submit feedback
async function submitFeedback(feedbackData) {
    try {
        const response = await fetch(`${API_BASE_URL}/feedback`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(feedbackData)
        });
        
        const result = await response.json();
        
        if (result.success) {
            alert(result.message);
            return true;
        } else {
            alert('Error: ' + result.error.message);
            return false;
        }
    } catch (error) {
        console.error('Error submitting feedback:', error);
        alert('Failed to submit feedback. Please try again.');
        return false;
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    // Fetch and render test sites
    fetchTestSites();
    
    // ... existing code ...
});
```

---

## 🧪 Testing Strategy

### Manual Testing

#### Test GET /api/test-sites
```bash
curl http://localhost:5000/api/test-sites
```

#### Test POST /api/contact
```bash
curl -X POST http://localhost:5000/api/contact \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "subject": "Test",
    "message": "This is a test message"
  }'
```

#### Test POST /api/feedback
```bash
curl -X POST http://localhost:5000/api/feedback \
  -H "Content-Type: application/json" \
  -d '{
    "rating": 5,
    "comment": "Great tool!",
    "page": "test-sites"
  }'
```

### Automated Testing

Create `tests/test_api.py`:

```python
import pytest
from app import create_app, db

@pytest.fixture
def client():
    app = create_app('testing')
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_get_test_sites(client):
    response = client.get('/api/test-sites')
    assert response.status_code == 200
    assert response.json['success'] == True
    assert len(response.json['data']) == 6

def test_submit_contact(client):
    data = {
        'name': 'Test User',
        'email': 'test@example.com',
        'subject': 'Test Subject',
        'message': 'This is a test message'
    }
    response = client.post('/api/contact', json=data)
    assert response.status_code == 201
    assert response.json['success'] == True

def test_submit_feedback(client):
    data = {
        'rating': 5,
        'comment': 'Great tool!',
        'page': 'test-sites'
    }
    response = client.post('/api/feedback', json=data)
    assert response.status_code == 201
    assert response.json['success'] == True
```

Run tests:
```bash
pytest tests/
```

---

## 🚀 Deployment

### Development Server

```bash
cd backend
python app.py
```

Server runs at: `http://localhost:5000`

### Production Server (Gunicorn)

Install gunicorn:
```bash
pip install gunicorn
```

Run with gunicorn:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Environment Variables

Production `.env`:
```env
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-production-secret-key
DATABASE_URL=sqlite:///data/webscraper.db
CORS_ORIGINS=https://yourdomain.com
```

---

## 📊 Success Metrics

### Functionality Checklist
- [ ] GET /api/test-sites returns all test sites
- [ ] GET /api/test-sites/:id returns single test site
- [ ] POST /api/contact validates and stores contact
- [ ] POST /api/feedback validates and stores feedback
- [ ] GET /api/health returns server status
- [ ] CORS allows frontend requests
- [ ] Database stores data correctly
- [ ] Validation catches invalid inputs
- [ ] Error responses are consistent

### Performance Targets
- API response time < 100ms
- Database queries < 50ms
- Handle 100 concurrent requests
- Zero memory leaks

### Code Quality
- 100% test coverage for critical paths
- No linting errors
- Consistent code formatting
- Comprehensive documentation

---

## 🔮 Future Enhancements

### Phase 2 Features
- [ ] User authentication (JWT)
- [ ] Admin dashboard
- [ ] Email notifications
- [ ] Rate limiting
- [ ] Response caching
- [ ] Pagination for large datasets
- [ ] Search and filtering
- [ ] Export data (CSV, JSON)

### Phase 3 Features
- [ ] PostgreSQL support
- [ ] Redis caching
- [ ] WebSocket support
- [ ] File uploads
- [ ] Analytics dashboard
- [ ] API versioning
- [ ] GraphQL endpoint

---

## 📚 Resources

### Documentation
- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Marshmallow Documentation](https://marshmallow.readthedocs.io/)

### Tutorials
- Flask REST API Tutorial
- SQLAlchemy ORM Guide
- API Design Best Practices

---

## 🤝 Contributing

### Development Workflow
1. Create feature branch
2. Implement changes
3. Write tests
4. Run linting
5. Submit pull request

### Code Standards
- Follow PEP 8
- Write docstrings
- Add type hints
- Keep functions small
- Write tests

---

## 📝 Notes

### Design Decisions
- **SQLite**: Chosen for simplicity and portability
- **Marshmallow**: Provides robust validation
- **Blueprint**: Modular route organization
- **JSON Response**: Consistent API format

### Known Limitations
- SQLite not suitable for high concurrency
- No authentication in v1.0
- No rate limiting in v1.0
- Basic error handling

### Migration Path
- Can migrate to PostgreSQL later
- Can add authentication layer
- Can implement caching
- Can add more endpoints

---

## ✅ Completion Checklist

### Setup
- [ ] Create backend directory structure
- [ ] Install dependencies
- [ ] Configure environment variables
- [ ] Initialize database

### Implementation
- [ ] Create Flask application
- [ ] Implement database models
- [ ] Create validation schemas
- [ ] Build API routes
- [ ] Add error handling
- [ ] Create test data

### Testing
- [ ] Manual API testing
- [ ] Write automated tests
- [ ] Test CORS functionality
- [ ] Test validation rules

### Integration
- [ ] Update frontend JavaScript
- [ ] Test frontend-backend communication
- [ ] Handle loading states
- [ ] Handle errors gracefully

### Documentation
- [ ] API documentation
- [ ] Code comments
- [ ] README updates
- [ ] Testing guide

---

**Status**: Ready for Implementation  
**Estimated Time**: 4-6 hours  
**Difficulty**: Intermediate  

**Next Step**: Begin Phase 1 - Project Setup

---

*Built with Flask, SQLAlchemy, and Marshmallow* 🚀

---

## 🔴 Security Workshop - Vulnerable Code Examples

**⚠️ WARNING: The following code contains intentional security vulnerabilities for educational purposes only!**

This section provides vulnerable code examples that SAST tools should detect. Each vulnerability includes:
- Vulnerable code example
- Security issue description
- SAST tool detection
- Secure alternative

---

### Vulnerability 1: SQL Injection

**Severity**: CRITICAL  
**CWE**: CWE-89  
**OWASP**: A03:2021 - Injection

**Vulnerable Code** (`routes/vulnerable_api.py`):
```python
from flask import Blueprint, request, jsonify
import sqlite3

vulnerable_bp = Blueprint('vulnerable', __name__)

@vulnerable_bp.route('/search', methods=['GET'])
def search_contacts():
    """VULNERABLE: SQL Injection"""
    search_term = request.args.get('q', '')
    
    # VULNERABILITY: Direct string concatenation in SQL query
    conn = sqlite3.connect('data/webscraper.db')
    cursor = conn.cursor()
    query = f"SELECT * FROM contacts WHERE name LIKE '%{search_term}%'"
    cursor.execute(query)  # Bandit: B608
    results = cursor.fetchall()
    conn.close()
    
    return jsonify({'results': results})
```

**Attack Example**:
```bash
# Attacker can inject SQL
curl "http://localhost:5000/api/search?q='; DROP TABLE contacts; --"
```

**SAST Detection**:
- Bandit: B608 (hardcoded SQL string)
- SonarQube: S2077 (SQL injection)
- Semgrep: python.lang.security.audit.sql-injection

**Secure Alternative**:
```python
@vulnerable_bp.route('/search', methods=['GET'])
def search_contacts_secure():
    """SECURE: Using parameterized queries"""
    search_term = request.args.get('q', '')
    
    conn = sqlite3.connect('data/webscraper.db')
    cursor = conn.cursor()
    # Use parameterized query
    query = "SELECT * FROM contacts WHERE name LIKE ?"
    cursor.execute(query, (f'%{search_term}%',))
    results = cursor.fetchall()
    conn.close()
    
    return jsonify({'results': results})
```

---

### Vulnerability 2: Hardcoded Credentials

**Severity**: HIGH  
**CWE**: CWE-798  
**OWASP**: A07:2021 - Identification and Authentication Failures

**Vulnerable Code** (`config.py`):
```python
class Config:
    # VULNERABILITY: Hardcoded credentials
    SECRET_KEY = 'super-secret-key-12345'  # Bandit: B105
    DATABASE_PASSWORD = 'admin123'  # Bandit: B105
    API_KEY = 'sk-1234567890abcdef'  # Bandit: B105
    
    # VULNERABILITY: Hardcoded database connection
    SQLALCHEMY_DATABASE_URI = 'postgresql://admin:password123@localhost/db'  # Bandit: B105
```

**SAST Detection**:
- Bandit: B105 (hardcoded password string)
- SonarQube: S2068 (credentials should not be hard-coded)
- Snyk: Hardcoded secrets

**Secure Alternative**:
```python
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Use environment variables
    SECRET_KEY = os.getenv('SECRET_KEY')
    DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
    API_KEY = os.getenv('API_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
```

---

### Vulnerability 3: Command Injection

**Severity**: CRITICAL  
**CWE**: CWE-78  
**OWASP**: A03:2021 - Injection

**Vulnerable Code** (`utils/file_operations.py`):
```python
import os
import subprocess

def backup_database(filename):
    """VULNERABLE: Command Injection"""
    # VULNERABILITY: Using shell=True with user input
    backup_path = f"/backups/{filename}"
    command = f"cp data/webscraper.db {backup_path}"
    subprocess.call(command, shell=True)  # Bandit: B602, B607
    
    return f"Backup created at {backup_path}"

def list_files(directory):
    """VULNERABLE: Command Injection via os.system"""
    # VULNERABILITY: Direct execution of user input
    os.system(f"ls -la {directory}")  # Bandit: B605, B607
```

**Attack Example**:
```python
# Attacker can inject commands
backup_database("backup.db; rm -rf /")
list_files("/tmp; cat /etc/passwd")
```

**SAST Detection**:
- Bandit: B602 (shell=True), B605 (os.system), B607 (partial shell path)
- SonarQube: S4721 (OS command injection)
- Semgrep: python.lang.security.audit.dangerous-subprocess-use

**Secure Alternative**:
```python
import shutil
import subprocess
from pathlib import Path

def backup_database_secure(filename):
    """SECURE: Using safe file operations"""
    # Validate filename
    if not filename.endswith('.db'):
        raise ValueError("Invalid filename")
    
    # Use safe path operations
    backup_path = Path("/backups") / filename
    shutil.copy2("data/webscraper.db", backup_path)
    
    return f"Backup created at {backup_path}"

def list_files_secure(directory):
    """SECURE: Using subprocess with list arguments"""
    # Use list of arguments instead of shell string
    result = subprocess.run(
        ["ls", "-la", directory],
        shell=False,  # Never use shell=True with user input
        capture_output=True,
        text=True
    )
    return result.stdout
```

---

### Vulnerability 4: Path Traversal

**Severity**: HIGH  
**CWE**: CWE-22  
**OWASP**: A01:2021 - Broken Access Control

**Vulnerable Code** (`routes/file_api.py`):
```python
from flask import Blueprint, send_file, request

file_bp = Blueprint('files', __name__)

@file_bp.route('/download', methods=['GET'])
def download_file():
    """VULNERABLE: Path Traversal"""
    filename = request.args.get('file')
    
    # VULNERABILITY: No path validation
    file_path = f"data/{filename}"
    return send_file(file_path)  # Attacker can use ../../../etc/passwd
```

**Attack Example**:
```bash
# Attacker can access any file on the system
curl "http://localhost:5000/api/download?file=../../../etc/passwd"
curl "http://localhost:5000/api/download?file=../../config.py"
```

**SAST Detection**:
- Bandit: B108 (hardcoded /tmp directory)
- SonarQube: S5131 (path traversal)
- Semgrep: python.flask.security.audit.path-traversal

**Secure Alternative**:
```python
from flask import Blueprint, send_file, request, abort
from pathlib import Path
import os

file_bp = Blueprint('files', __name__)

@file_bp.route('/download', methods=['GET'])
def download_file_secure():
    """SECURE: Path validation"""
    filename = request.args.get('file')
    
    # Validate filename
    if not filename or '..' in filename or filename.startswith('/'):
        abort(400, "Invalid filename")
    
    # Use safe path resolution
    base_dir = Path("data").resolve()
    file_path = (base_dir / filename).resolve()
    
    # Ensure file is within allowed directory
    if not str(file_path).startswith(str(base_dir)):
        abort(403, "Access denied")
    
    if not file_path.exists():
        abort(404, "File not found")
    
    return send_file(file_path)
```

---

### Vulnerability 5: Insecure Deserialization

**Severity**: CRITICAL  
**CWE**: CWE-502  
**OWASP**: A08:2021 - Software and Data Integrity Failures

**Vulnerable Code** (`utils/session_manager.py`):
```python
import pickle
import base64
from flask import request

def load_user_session():
    """VULNERABLE: Insecure Deserialization"""
    session_data = request.cookies.get('session')
    
    if session_data:
        # VULNERABILITY: Unpickling untrusted data
        decoded = base64.b64decode(session_data)
        user_data = pickle.loads(decoded)  # Bandit: B301
        return user_data
    
    return None

def save_user_session(user_data):
    """VULNERABLE: Using pickle for serialization"""
    # VULNERABILITY: Pickle can execute arbitrary code
    serialized = pickle.dumps(user_data)  # Bandit: B301
    encoded = base64.b64encode(serialized)
    return encoded
```

**Attack Example**:
```python
# Attacker can create malicious pickle payload
import pickle
import base64

class Exploit:
    def __reduce__(self):
        import os
        return (os.system, ('rm -rf /',))

malicious = base64.b64encode(pickle.dumps(Exploit()))
# Send as cookie to execute arbitrary code
```

**SAST Detection**:
- Bandit: B301 (pickle usage)
- SonarQube: S5135 (insecure deserialization)
- Semgrep: python.lang.security.audit.dangerous-pickle-use

**Secure Alternative**:
```python
import json
from flask import request
from itsdangerous import URLSafeTimedSerializer

serializer = URLSafeTimedSerializer('secret-key')

def load_user_session_secure():
    """SECURE: Using JSON with signed tokens"""
    session_data = request.cookies.get('session')
    
    if session_data:
        try:
            # Use signed serializer instead of pickle
            user_data = serializer.loads(session_data, max_age=3600)
            return user_data
        except Exception:
            return None
    
    return None

def save_user_session_secure(user_data):
    """SECURE: Using JSON serialization"""
    # Use JSON instead of pickle
    return serializer.dumps(user_data)
```

---

### Vulnerability 6: Weak Cryptography

**Severity**: MEDIUM  
**CWE**: CWE-327  
**OWASP**: A02:2021 - Cryptographic Failures

**Vulnerable Code** (`utils/crypto.py`):
```python
import hashlib
import random

def hash_password(password):
    """VULNERABLE: Weak hashing algorithm"""
    # VULNERABILITY: MD5 is cryptographically broken
    return hashlib.md5(password.encode()).hexdigest()  # Bandit: B303, B324

def generate_token():
    """VULNERABLE: Weak random number generator"""
    # VULNERABILITY: random is not cryptographically secure
    return str(random.randint(100000, 999999))  # Bandit: B311

def encrypt_data(data, key):
    """VULNERABLE: Weak encryption"""
    # VULNERABILITY: XOR is not secure encryption
    encrypted = ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(data))
    return encrypted
```

**SAST Detection**:
- Bandit: B303 (MD5), B324 (hashlib), B311 (random)
- SonarQube: S4790 (weak hashing), S2245 (weak random)
- Semgrep: python.lang.security.audit.weak-crypto

**Secure Alternative**:
```python
import hashlib
import secrets
from cryptography.fernet import Fernet

def hash_password_secure(password):
    """SECURE: Using bcrypt or Argon2"""
    import bcrypt
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt)

def generate_token_secure():
    """SECURE: Using secrets module"""
    return secrets.token_urlsafe(32)

def encrypt_data_secure(data, key):
    """SECURE: Using Fernet (AES)"""
    f = Fernet(key)
    return f.encrypt(data.encode())
```

---

### Vulnerability 7: XML External Entity (XXE)

**Severity**: HIGH  
**CWE**: CWE-611  
**OWASP**: A05:2021 - Security Misconfiguration

**Vulnerable Code** (`utils/xml_parser.py`):
```python
import xml.etree.ElementTree as ET
from lxml import etree

def parse_xml_config(xml_string):
    """VULNERABLE: XXE Attack"""
    # VULNERABILITY: Default XML parser allows external entities
    root = ET.fromstring(xml_string)  # Bandit: B314
    return root

def parse_xml_lxml(xml_string):
    """VULNERABLE: XXE with lxml"""
    # VULNERABILITY: lxml parser without security settings
    parser = etree.XMLParser()  # Bandit: B320
    root = etree.fromstring(xml_string, parser)
    return root
```

**Attack Example**:
```xml
<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<config>
  <data>&xxe;</data>
</config>
```

**SAST Detection**:
- Bandit: B314 (xml.etree.ElementTree), B320 (lxml)
- SonarQube: S2755 (XXE vulnerability)
- Semgrep: python.lang.security.audit.xxe

**Secure Alternative**:
```python
import defusedxml.ElementTree as ET
from lxml import etree

def parse_xml_config_secure(xml_string):
    """SECURE: Using defusedxml"""
    # Use defusedxml to prevent XXE
    root = ET.fromstring(xml_string)
    return root

def parse_xml_lxml_secure(xml_string):
    """SECURE: Disable external entities"""
    parser = etree.XMLParser(
        resolve_entities=False,
        no_network=True,
        dtd_validation=False
    )
    root = etree.fromstring(xml_string, parser)
    return root
```

---

### Vulnerability 8: Server-Side Request Forgery (SSRF)

**Severity**: HIGH  
**CWE**: CWE-918  
**OWASP**: A10:2021 - Server-Side Request Forgery

**Vulnerable Code** (`routes/proxy_api.py`):
```python
from flask import Blueprint, request, jsonify
import requests

proxy_bp = Blueprint('proxy', __name__)

@proxy_bp.route('/fetch', methods=['GET'])
def fetch_url():
    """VULNERABLE: SSRF"""
    url = request.args.get('url')
    
    # VULNERABILITY: No URL validation
    response = requests.get(url)  # Attacker can access internal services
    return jsonify({
        'content': response.text,
        'status': response.status_code
    })
```

**Attack Example**:
```bash
# Attacker can access internal services
curl "http://localhost:5000/api/fetch?url=http://localhost:6379"  # Redis
curl "http://localhost:5000/api/fetch?url=http://169.254.169.254/latest/meta-data/"  # AWS metadata
curl "http://localhost:5000/api/fetch?url=file:///etc/passwd"  # Local files
```

**SAST Detection**:
- SonarQube: S5144 (SSRF)
- Semgrep: python.flask.security.audit.ssrf

**Secure Alternative**:
```python
from flask import Blueprint, request, jsonify, abort
import requests
from urllib.parse import urlparse

proxy_bp = Blueprint('proxy', __name__)

ALLOWED_DOMAINS = ['api.example.com', 'cdn.example.com']
BLOCKED_IPS = ['127.0.0.1', 'localhost', '0.0.0.0']

@proxy_bp.route('/fetch', methods=['GET'])
def fetch_url_secure():
    """SECURE: URL validation"""
    url = request.args.get('url')
    
    # Validate URL
    try:
        parsed = urlparse(url)
        
        # Check protocol
        if parsed.scheme not in ['http', 'https']:
            abort(400, "Invalid protocol")
        
        # Check domain whitelist
        if parsed.hostname not in ALLOWED_DOMAINS:
            abort(403, "Domain not allowed")
        
        # Block internal IPs
        if parsed.hostname in BLOCKED_IPS:
            abort(403, "Access denied")
        
        # Make request with timeout
        response = requests.get(url, timeout=5, allow_redirects=False)
        
        return jsonify({
            'content': response.text[:1000],  # Limit response size
            'status': response.status_code
        })
    except Exception as e:
        abort(400, str(e))
```

---

### Vulnerability 9: Debug Mode in Production

**Severity**: MEDIUM  
**CWE**: CWE-489  
**OWASP**: A05:2021 - Security Misconfiguration

**Vulnerable Code** (`app.py`):
```python
from flask import Flask

app = Flask(__name__)

# VULNERABILITY: Debug mode enabled
app.config['DEBUG'] = True  # Bandit: B201
app.config['TESTING'] = True

if __name__ == '__main__':
    # VULNERABILITY: Running with debug=True
    app.run(host='0.0.0.0', port=5000, debug=True)  # Bandit: B201
```

**Security Issues**:
- Exposes stack traces with sensitive information
- Enables code execution via debugger
- Shows source code in error pages
- Allows arbitrary code execution

**SAST Detection**:
- Bandit: B201 (Flask debug mode)
- SonarQube: S4507 (debug features enabled)

**Secure Alternative**:
```python
from flask import Flask
import os

app = Flask(__name__)

# Use environment variable
app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'False') == 'True'

if __name__ == '__main__':
    # Never use debug=True in production
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False
    )
```

---

### Vulnerability 10: Insufficient Input Validation

**Severity**: MEDIUM  
**CWE**: CWE-20  
**OWASP**: A03:2021 - Injection

**Vulnerable Code** (`routes/user_api.py`):
```python
from flask import Blueprint, request, jsonify
import re

user_bp = Blueprint('user', __name__)

@user_bp.route('/register', methods=['POST'])
def register_user():
    """VULNERABLE: Insufficient validation"""
    data = request.get_json()
    
    # VULNERABILITY: No input validation
    username = data.get('username')
    email = data.get('email')
    age = data.get('age')
    
    # VULNERABILITY: Unsafe regex (ReDoS)
    email_pattern = r'^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$'
    if not re.match(email_pattern, email):  # Bandit: B105 (complex regex)
        return jsonify({'error': 'Invalid email'}), 400
    
    # VULNERABILITY: No length limits
    # VULNERABILITY: No type checking
    # VULNERABILITY: No sanitization
    
    return jsonify({'message': 'User registered'}), 201
```

**Attack Examples**:
```python
# ReDoS attack
email = "a" * 10000 + "@example.com"

# Type confusion
age = "not a number"

# Injection via username
username = "<script>alert('XSS')</script>"
```

**SAST Detection**:
- Bandit: B105 (complex regex)
- SonarQube: S5852 (ReDoS), S2631 (regex complexity)

**Secure Alternative**:
```python
from flask import Blueprint, request, jsonify
from marshmallow import Schema, fields, validate, ValidationError
import bleach

class UserSchema(Schema):
    username = fields.Str(
        required=True,
        validate=[
            validate.Length(min=3, max=50),
            validate.Regexp(r'^[a-zA-Z0-9_]+$')
        ]
    )
    email = fields.Email(required=True)
    age = fields.Int(
        required=True,
        validate=validate.Range(min=13, max=120)
    )

user_bp = Blueprint('user', __name__)

@user_bp.route('/register', methods=['POST'])
def register_user_secure():
    """SECURE: Proper validation"""
    schema = UserSchema()
    
    try:
        # Validate input
        data = schema.load(request.get_json())
        
        # Sanitize HTML
        username = bleach.clean(data['username'])
        
        # Process validated data
        return jsonify({'message': 'User registered'}), 201
        
    except ValidationError as e:
        return jsonify({'errors': e.messages}), 400
```

---

## 🔍 SAST Tool Configuration

### Bandit Configuration (`.bandit`)

```yaml
# .bandit
tests:
  - B101  # assert_used
  - B105  # hardcoded_password_string
  - B106  # hardcoded_password_funcarg
  - B107  # hardcoded_password_default
  - B108  # hardcoded_tmp_directory
  - B201  # flask_debug_true
  - B301  # pickle
  - B303  # md5
  - B311  # random
  - B314  # xml_bad_etree
  - B320  # xml_bad_lxml
  - B324  # hashlib
  - B602  # shell_true
  - B605  # start_process_with_a_shell
  - B607  # start_process_with_partial_path
  - B608  # hardcoded_sql_expressions

exclude_dirs:
  - /tests/
  - /venv/
```

### Running SAST Tools

```bash
# Bandit
pip install bandit
bandit -r backend/ -f json -o bandit-report.json

# Safety (dependency check)
pip install safety
safety check --json

# Semgrep
pip install semgrep
semgrep --config=auto backend/

# Snyk
npm install -g snyk
snyk test --file=requirements.txt
```

---

## 📊 Expected SAST Findings Summary

| Vulnerability | Severity | CWE | Tools Detecting |
|---------------|----------|-----|-----------------|
| SQL Injection | Critical | CWE-89 | Bandit, SonarQube, Semgrep |
| Hardcoded Credentials | High | CWE-798 | Bandit, SonarQube, Snyk |
| Command Injection | Critical | CWE-78 | Bandit, SonarQube, Semgrep |
| Path Traversal | High | CWE-22 | SonarQube, Semgrep |
| Insecure Deserialization | Critical | CWE-502 | Bandit, SonarQube, Semgrep |
| Weak Cryptography | Medium | CWE-327 | Bandit, SonarQube, Semgrep |
| XXE | High | CWE-611 | Bandit, SonarQube, Semgrep |
| SSRF | High | CWE-918 | SonarQube, Semgrep |
| Debug Mode | Medium | CWE-489 | Bandit, SonarQube |
| Insufficient Validation | Medium | CWE-20 | Bandit, SonarQube |

---

## 🎓 Workshop Learning Objectives

By working with these vulnerable code examples, participants will learn to:

1. **Identify Security Vulnerabilities**
   - Recognize common security anti-patterns
   - Understand OWASP Top 10 vulnerabilities
   - Read and interpret SAST tool reports

2. **Use SAST Tools**
   - Configure and run Bandit
   - Interpret security findings
   - Prioritize vulnerabilities by severity

3. **Remediate Security Issues**
   - Apply secure coding practices
   - Implement proper input validation
   - Use secure libraries and functions

4. **Prevent Future Vulnerabilities**
   - Integrate SAST into CI/CD pipeline
   - Establish secure coding standards
   - Conduct security code reviews

---

## ⚠️ IMPORTANT REMINDERS

1. **Never use vulnerable code in production**
2. **Always validate and sanitize user input**
3. **Use parameterized queries for database operations**
4. **Never hardcode credentials**
5. **Keep dependencies updated**
6. **Enable SAST tools in your CI/CD pipeline**
7. **Conduct regular security audits**
8. **Follow the principle of least privilege**
9. **Implement defense in depth**
10. **Stay informed about new vulnerabilities**

---

*This workshop material is designed for educational purposes to teach secure coding practices through hands-on experience with vulnerability detection and remediation.*