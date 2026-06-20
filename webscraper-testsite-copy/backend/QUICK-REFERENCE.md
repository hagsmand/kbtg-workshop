# Flask Backend - Quick Reference Card

## 🚀 Quick Start

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python run.py
```

Server: `http://localhost:5000`

---

## 📡 API Endpoints

### Secure Endpoints

```bash
# Get all test sites
GET /api/test-sites

# Get single test site
GET /api/test-sites/1

# Submit contact
POST /api/contact
{
  "name": "John Doe",
  "email": "john@example.com",
  "subject": "Question",
  "message": "Your message here"
}

# Submit feedback
POST /api/feedback
{
  "rating": 5,
  "comment": "Great tool!",
  "page": "test-sites"
}

# Health check
GET /api/health
```

### Vulnerable Endpoints (Training Only)

```bash
# Get vulnerability info
GET /api/vulnerable/info

# SQL Injection
GET /api/vulnerable/search?q=test

# Command Injection
POST /api/vulnerable/backup
{"filename": "backup.db"}

# Path Traversal
GET /api/vulnerable/download?file=test.txt

# More vulnerabilities...
```

---

## 🔍 SAST Commands

### Bandit

```bash
# Basic scan
bandit -r .

# JSON output
bandit -r . -f json -o report.json

# High severity only
bandit -r . -ll

# Specific tests
bandit -r . -t B105,B201,B608
```

### Semgrep

```bash
# Auto config
semgrep --config=auto .

# Security audit
semgrep --config=p/security-audit .

# Specific rules
semgrep --config=p/owasp-top-ten .
```

### Safety

```bash
# Check dependencies
safety check

# JSON output
safety check --json

# Full report
safety check --full-report
```

---

## 🐛 Vulnerabilities Reference

| ID | Vulnerability | CWE | Severity | Location |
|----|---------------|-----|----------|----------|
| 1 | SQL Injection | 89 | CRITICAL | vulnerable_api.py:32 |
| 2 | Command Injection | 78 | CRITICAL | vulnerable_api.py:52 |
| 3 | OS Command Injection | 78 | CRITICAL | vulnerable_api.py:75 |
| 4 | Path Traversal | 22 | HIGH | vulnerable_api.py:95 |
| 5 | Insecure Deserialization | 502 | CRITICAL | vulnerable_api.py:125 |
| 6 | Weak Crypto (MD5) | 327 | MEDIUM | vulnerable_api.py:150 |
| 7 | Weak Random | 338 | MEDIUM | vulnerable_api.py:170 |
| 8 | SSRF | 918 | HIGH | vulnerable_api.py:185 |
| 9 | Code Injection | 94 | CRITICAL | vulnerable_api.py:210 |
| 10 | Hardcoded Credentials | 798 | HIGH | config.py:13-15 |
| 11 | Debug Mode | 489 | MEDIUM | config.py:35, app.py:69 |

---

## 🔧 Common Fixes

### SQL Injection
```python
# ❌ Vulnerable
query = f"SELECT * FROM users WHERE name = '{name}'"

# ✅ Secure
query = "SELECT * FROM users WHERE name = ?"
cursor.execute(query, (name,))
```

### Command Injection
```python
# ❌ Vulnerable
os.system(f"ls {directory}")

# ✅ Secure
subprocess.run(['ls', directory], shell=False)
```

### Path Traversal
```python
# ❌ Vulnerable
file_path = f"data/{filename}"

# ✅ Secure
from pathlib import Path
base = Path("data").resolve()
file_path = (base / filename).resolve()
if not str(file_path).startswith(str(base)):
    raise ValueError("Invalid path")
```

### Hardcoded Secrets
```python
# ❌ Vulnerable
SECRET_KEY = 'hardcoded-secret'

# ✅ Secure
import os
SECRET_KEY = os.getenv('SECRET_KEY')
```

### Weak Crypto
```python
# ❌ Vulnerable
import hashlib
hash = hashlib.md5(password.encode()).hexdigest()

# ✅ Secure
import bcrypt
hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
```

---

## 📁 File Structure

```
backend/
├── app.py              # Main application
├── config.py           # Configuration
├── run.py              # Quick start script
├── requirements.txt    # Dependencies
├── routes/
│   ├── api.py         # Secure endpoints
│   ├── health.py      # Health check
│   └── vulnerable_api.py  # Vulnerable endpoints
├── models/
│   ├── contact.py     # Contact model
│   └── feedback.py    # Feedback model
├── schemas/
│   ├── contact.py     # Contact validation
│   └── feedback.py    # Feedback validation
└── data/
    └── test_sites.json  # Test data
```

---

## 🔑 Environment Variables

```bash
# .env file
FLASK_APP=app.py
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///data/webscraper.db
CORS_ORIGINS=http://localhost:8000
```

---

## 🧪 Testing

```bash
# Test health endpoint
curl http://localhost:5000/api/health

# Test GET endpoint
curl http://localhost:5000/api/test-sites

# Test POST endpoint
curl -X POST http://localhost:5000/api/contact \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","email":"test@example.com","subject":"Test","message":"Test message"}'
```

---

## 🐞 Troubleshooting

### Port in use
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:5000 | xargs kill -9
```

### Database locked
```bash
rm data/webscraper.db
python app.py
```

### Import errors
```bash
pip install -r requirements.txt --force-reinstall
```

### Virtual environment
```bash
# Deactivate
deactivate

# Reactivate
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

---

## 📊 Bandit Issue Codes

| Code | Issue | Severity |
|------|-------|----------|
| B105 | Hardcoded password | HIGH |
| B201 | Flask debug=True | HIGH |
| B301 | Pickle usage | MEDIUM |
| B303 | MD5 usage | MEDIUM |
| B307 | eval() usage | HIGH |
| B311 | random usage | LOW |
| B324 | hashlib weak | MEDIUM |
| B602 | shell=True | HIGH |
| B605 | shell command | HIGH |
| B607 | Partial path | LOW |
| B608 | SQL string | MEDIUM |

---

## 🎯 Workshop Checklist

- [ ] Install dependencies
- [ ] Start server
- [ ] Test endpoints
- [ ] Run Bandit scan
- [ ] Identify vulnerabilities
- [ ] Fix 3 issues
- [ ] Re-scan and verify
- [ ] Document changes

---

## 📚 Resources

- **Documentation**: `README.md`
- **Implementation Plan**: `FLASK-BACKEND-PLAN.md`
- **Workshop Guide**: `WORKSHOP-GUIDE.md`
- **Summary**: `BACKEND-IMPLEMENTATION-SUMMARY.md`

---

## ⚠️ Important

**DO NOT USE IN PRODUCTION!**

This backend contains intentional vulnerabilities for training purposes only.

---

**Quick Help**: `curl http://localhost:5000/api/vulnerable/info`