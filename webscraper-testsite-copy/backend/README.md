# Flask Backend API - Web Scraper Test Sites

⚠️ **WARNING: This backend contains intentional security vulnerabilities for SAST workshop training purposes. DO NOT USE IN PRODUCTION!**

## Overview

This Flask backend provides REST API endpoints for the Web Scraper Test Sites application, including both secure and intentionally vulnerable endpoints for security training.

## Features

- ✅ RESTful API design
- ✅ SQLite database with SQLAlchemy ORM
- ✅ Input validation with Marshmallow
- ✅ CORS support for frontend communication
- ✅ Secure endpoints following best practices
- ⚠️ Vulnerable endpoints for SAST training

## Project Structure

```
backend/
├── app.py                      # Main Flask application
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
│
├── routes/                    # API route handlers
│   ├── api.py                # Secure API endpoints
│   ├── health.py             # Health check endpoint
│   └── vulnerable_api.py     # Vulnerable endpoints (training)
│
├── models/                    # Database models
│   ├── contact.py            # Contact model
│   └── feedback.py           # Feedback model
│
├── schemas/                   # Validation schemas
│   ├── contact.py            # Contact validation
│   └── feedback.py           # Feedback validation
│
├── utils/                     # Utility functions
│   └── responses.py          # Response formatters
│
└── data/                      # Data files
    ├── test_sites.json       # Test sites data
    └── webscraper.db         # SQLite database (generated)
```

## Installation

### 1. Create Virtual Environment

```bash
cd backend
python -m venv venv
```

### 2. Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
copy .env.example .env
# Edit .env with your settings
```

## Running the Server

### Development Mode

```bash
python app.py
```

Server will start at: `http://localhost:5000`

### Production Mode (with Gunicorn)

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## API Endpoints

### Secure Endpoints

#### GET /api/test-sites
Get all test sites
```bash
curl http://localhost:5000/api/test-sites
```

#### GET /api/test-sites/:id
Get single test site
```bash
curl http://localhost:5000/api/test-sites/1
```

#### POST /api/contact
Submit contact form
```bash
curl -X POST http://localhost:5000/api/contact \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "subject": "Question",
    "message": "This is a test message"
  }'
```

#### POST /api/feedback
Submit feedback
```bash
curl -X POST http://localhost:5000/api/feedback \
  -H "Content-Type: application/json" \
  -d '{
    "rating": 5,
    "comment": "Great tool!",
    "page": "test-sites"
  }'
```

#### GET /api/health
Health check
```bash
curl http://localhost:5000/api/health
```

### Vulnerable Endpoints (Training Only)

⚠️ **DO NOT USE THESE IN PRODUCTION!**

#### GET /api/vulnerable/info
Get information about vulnerable endpoints
```bash
curl http://localhost:5000/api/vulnerable/info
```

See `FLASK-BACKEND-PLAN.md` for complete documentation of all vulnerable endpoints.

## SAST Workshop

### Running Security Scans

#### Bandit (Python Security Linter)

```bash
pip install bandit
bandit -r . -f json -o bandit-report.json
```

#### Safety (Dependency Checker)

```bash
pip install safety
safety check --json
```

#### Semgrep

```bash
pip install semgrep
semgrep --config=auto .
```

### Expected Vulnerabilities

The vulnerable endpoints contain these intentional security issues:

1. **SQL Injection** (CWE-89) - CRITICAL
2. **Command Injection** (CWE-78) - CRITICAL
3. **Path Traversal** (CWE-22) - HIGH
4. **Insecure Deserialization** (CWE-502) - CRITICAL
5. **Weak Cryptography** (CWE-327) - MEDIUM
6. **Weak Random** (CWE-338) - MEDIUM
7. **SSRF** (CWE-918) - HIGH
8. **Code Injection** (CWE-94) - CRITICAL
9. **Hardcoded Credentials** (CWE-798) - HIGH
10. **Debug Mode** (CWE-489) - MEDIUM

## Database

### Schema

**contacts table:**
- id (INTEGER PRIMARY KEY)
- name (VARCHAR 100)
- email (VARCHAR 255)
- subject (VARCHAR 200)
- message (TEXT)
- status (VARCHAR 20)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)

**feedback table:**
- id (INTEGER PRIMARY KEY)
- rating (INTEGER 1-5)
- comment (TEXT)
- page (VARCHAR 100)
- email (VARCHAR 255)
- user_agent (TEXT)
- ip_address (VARCHAR 45)
- created_at (TIMESTAMP)

### Database Management

The database is automatically created when you first run the application.

To reset the database:
```bash
rm data/webscraper.db
python app.py  # Will recreate tables
```

## Testing

### Manual Testing

Use curl, Postman, or any HTTP client to test the endpoints.

### Automated Testing

```bash
pytest tests/
```

## Security Notes

### For Workshop Participants

1. **Identify Vulnerabilities**: Use SAST tools to find security issues
2. **Understand Impact**: Learn what each vulnerability can do
3. **Learn Remediation**: Study the secure alternatives
4. **Practice Fixes**: Try fixing the vulnerable code

### For Production Use

**NEVER use the vulnerable endpoints in production!**

To make this production-ready:
1. Remove all `/api/vulnerable/*` endpoints
2. Change hardcoded credentials in `config.py`
3. Set `DEBUG = False`
4. Use environment variables for all secrets
5. Implement rate limiting
6. Add authentication/authorization
7. Use HTTPS
8. Implement logging and monitoring
9. Regular security audits
10. Keep dependencies updated

## Troubleshooting

### Port Already in Use

```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:5000 | xargs kill -9
```

### Database Locked

```bash
rm data/webscraper.db
python app.py
```

### Import Errors

```bash
pip install -r requirements.txt --force-reinstall
```

## Contributing

This is a training project. Contributions should maintain the educational purpose while following security best practices for the secure endpoints.

## License

MIT License - For educational purposes only

## Disclaimer

⚠️ **IMPORTANT**: This application contains intentional security vulnerabilities for educational purposes. It is designed to teach developers about common security issues and how to detect them using SAST tools. 

**DO NOT**:
- Deploy this to production
- Use it with real user data
- Expose it to the internet
- Use the vulnerable code patterns in real applications

**DO**:
- Use it for learning
- Practice with SAST tools
- Study the secure alternatives
- Share knowledge with your team

---

**Built for KBTG Security Workshop** 🔒