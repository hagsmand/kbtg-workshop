# SAST Workshop Guide
## Using Flask Backend for Security Training

**Workshop Duration**: 2-3 hours  
**Skill Level**: Intermediate  
**Prerequisites**: Basic Python, Flask, and security knowledge

---

## 🎯 Workshop Objectives

By the end of this workshop, participants will be able to:

1. ✅ Run SAST tools (Bandit, Semgrep, SonarQube)
2. ✅ Identify common security vulnerabilities
3. ✅ Understand vulnerability severity and impact
4. ✅ Remediate security issues
5. ✅ Integrate SAST into development workflow

---

## 📋 Workshop Agenda

### Part 1: Setup (15 minutes)

1. **Environment Setup**
   ```bash
   cd backend
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Start the Server**
   ```bash
   python run.py
   ```

3. **Verify Installation**
   ```bash
   curl http://localhost:5000/api/health
   ```

### Part 2: Understanding the Code (20 minutes)

1. **Review Secure Endpoints**
   - Open `routes/api.py`
   - Study input validation
   - Understand error handling

2. **Review Vulnerable Endpoints**
   - Open `routes/vulnerable_api.py`
   - Identify security issues
   - Understand attack vectors

3. **Compare Implementations**
   - Side-by-side comparison
   - Spot the differences
   - Learn best practices

### Part 3: Running SAST Tools (30 minutes)

#### Exercise 1: Bandit Scan

```bash
# Install Bandit
pip install bandit

# Run basic scan
bandit -r .

# Run with JSON output
bandit -r . -f json -o bandit-report.json

# View specific issues
bandit -r . -ll  # Only show high severity
```

**Expected Findings**: 11+ security issues

**Tasks**:
- [ ] Run Bandit scan
- [ ] Count total findings
- [ ] Identify CRITICAL issues
- [ ] Note line numbers

#### Exercise 2: Analyze Findings

Review the Bandit report and categorize findings:

| Severity | Count | Examples |
|----------|-------|----------|
| HIGH | ? | B105, B201, B608 |
| MEDIUM | ? | B303, B311, B324 |
| LOW | ? | - |

**Tasks**:
- [ ] List all HIGH severity issues
- [ ] Understand each CWE
- [ ] Map to OWASP Top 10

#### Exercise 3: Semgrep Scan

```bash
# Install Semgrep
pip install semgrep

# Run scan
semgrep --config=auto .

# Run with specific rules
semgrep --config=p/security-audit .
```

**Tasks**:
- [ ] Compare Semgrep vs Bandit findings
- [ ] Note unique detections
- [ ] Understand rule sets

### Part 4: Vulnerability Deep Dive (45 minutes)

#### Vulnerability 1: SQL Injection

**Location**: `routes/vulnerable_api.py:32`

**Vulnerable Code**:
```python
query = f"SELECT * FROM contacts WHERE name LIKE '%{search_term}%'"
cursor.execute(query)
```

**Attack Example**:
```bash
curl "http://localhost:5000/api/vulnerable/search?q='; DROP TABLE contacts; --"
```

**Impact**:
- Data theft
- Data modification
- Data deletion
- Authentication bypass

**Remediation**:
```python
# Use parameterized queries
query = "SELECT * FROM contacts WHERE name LIKE ?"
cursor.execute(query, (f'%{search_term}%',))
```

**Tasks**:
- [ ] Test the vulnerable endpoint
- [ ] Understand the attack
- [ ] Implement the fix
- [ ] Verify with SAST

#### Vulnerability 2: Command Injection

**Location**: `routes/vulnerable_api.py:52`

**Vulnerable Code**:
```python
command = f"cp data/webscraper.db {backup_path}"
subprocess.call(command, shell=True)
```

**Attack Example**:
```bash
curl -X POST http://localhost:5000/api/vulnerable/backup \
  -H "Content-Type: application/json" \
  -d '{"filename": "backup.db; rm -rf /"}'
```

**Impact**:
- Arbitrary command execution
- System compromise
- Data destruction

**Remediation**:
```python
# Use list arguments, no shell
subprocess.run(['cp', 'data/webscraper.db', backup_path], shell=False)
```

**Tasks**:
- [ ] Test the vulnerable endpoint
- [ ] Understand shell=True risk
- [ ] Implement the fix
- [ ] Verify with SAST

#### Vulnerability 3: Path Traversal

**Location**: `routes/vulnerable_api.py:95`

**Vulnerable Code**:
```python
file_path = f"data/{filename}"
with open(file_path, 'r') as f:
    content = f.read()
```

**Attack Example**:
```bash
curl "http://localhost:5000/api/vulnerable/download?file=../../../etc/passwd"
```

**Impact**:
- Unauthorized file access
- Information disclosure
- Configuration exposure

**Remediation**:
```python
from pathlib import Path

base_dir = Path("data").resolve()
file_path = (base_dir / filename).resolve()

# Ensure file is within allowed directory
if not str(file_path).startswith(str(base_dir)):
    abort(403, "Access denied")
```

**Tasks**:
- [ ] Test the vulnerable endpoint
- [ ] Try path traversal attack
- [ ] Implement the fix
- [ ] Verify with SAST

### Part 5: Remediation Practice (40 minutes)

#### Exercise 4: Fix Vulnerabilities

Choose 3 vulnerabilities to fix:

1. **Hardcoded Credentials** (config.py)
   - [ ] Identify hardcoded secrets
   - [ ] Move to environment variables
   - [ ] Update .env.example
   - [ ] Verify with Bandit

2. **Weak Cryptography** (vulnerable_api.py)
   - [ ] Replace MD5 with bcrypt
   - [ ] Update hash_password function
   - [ ] Test with sample data
   - [ ] Verify with Bandit

3. **Debug Mode** (app.py, config.py)
   - [ ] Disable debug in production
   - [ ] Use environment variable
   - [ ] Test configuration
   - [ ] Verify with Bandit

#### Exercise 5: Verify Fixes

```bash
# Run Bandit again
bandit -r . -f json -o bandit-after.json

# Compare reports
# Before: 11+ issues
# After: Should be reduced
```

**Tasks**:
- [ ] Count remaining issues
- [ ] Verify fixes worked
- [ ] Document changes
- [ ] Create pull request

### Part 6: Integration & Best Practices (30 minutes)

#### Exercise 6: CI/CD Integration

Create a GitHub Actions workflow:

```yaml
name: Security Scan

on: [push, pull_request]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: |
          pip install bandit safety
      
      - name: Run Bandit
        run: bandit -r . -f json -o bandit-report.json
      
      - name: Run Safety
        run: safety check --json
      
      - name: Upload results
        uses: actions/upload-artifact@v2
        with:
          name: security-reports
          path: bandit-report.json
```

**Tasks**:
- [ ] Create workflow file
- [ ] Test locally
- [ ] Push to repository
- [ ] Review results

#### Exercise 7: Security Checklist

Create a security checklist for your team:

**Pre-Commit**:
- [ ] Run Bandit locally
- [ ] Fix HIGH severity issues
- [ ] Review MEDIUM issues
- [ ] Update documentation

**Code Review**:
- [ ] Check for hardcoded secrets
- [ ] Verify input validation
- [ ] Review error handling
- [ ] Check dependencies

**Pre-Deployment**:
- [ ] Run full SAST scan
- [ ] Review all findings
- [ ] Document exceptions
- [ ] Update security docs

---

## 🎓 Learning Outcomes

After completing this workshop, you should be able to:

### Knowledge
- ✅ Understand 10+ common vulnerabilities
- ✅ Know OWASP Top 10
- ✅ Understand CWE categories
- ✅ Know SAST tool capabilities

### Skills
- ✅ Run SAST tools
- ✅ Interpret findings
- ✅ Prioritize issues
- ✅ Fix vulnerabilities
- ✅ Verify remediation

### Practices
- ✅ Integrate SAST in workflow
- ✅ Conduct security reviews
- ✅ Document security decisions
- ✅ Share security knowledge

---

## 📊 Assessment

### Quiz Questions

1. **What is SQL Injection?**
   - How does it work?
   - How to prevent it?
   - What tools detect it?

2. **Why is shell=True dangerous?**
   - What's the risk?
   - What's the alternative?
   - How to detect it?

3. **What's wrong with MD5?**
   - Why is it weak?
   - What should you use?
   - How to migrate?

### Practical Assessment

Fix these vulnerabilities:
- [ ] SQL Injection in search endpoint
- [ ] Command Injection in backup endpoint
- [ ] Hardcoded credentials in config
- [ ] Debug mode in production
- [ ] Weak random token generation

**Passing Criteria**: Fix 4 out of 5 vulnerabilities

---

## 📚 Additional Resources

### Documentation
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CWE Top 25](https://cwe.mitre.org/top25/)
- [Bandit Docs](https://bandit.readthedocs.io/)
- [Semgrep Rules](https://semgrep.dev/explore)

### Tools
- [Bandit](https://github.com/PyCQA/bandit)
- [Semgrep](https://semgrep.dev/)
- [Safety](https://github.com/pyupio/safety)
- [Snyk](https://snyk.io/)

### Practice
- [OWASP WebGoat](https://owasp.org/www-project-webgoat/)
- [Damn Vulnerable Web App](http://www.dvwa.co.uk/)
- [HackTheBox](https://www.hackthebox.com/)

---

## 🤝 Workshop Tips

### For Instructors
1. Start with theory (15 min)
2. Demo SAST tools (15 min)
3. Hands-on exercises (90 min)
4. Group discussion (20 min)
5. Q&A and wrap-up (10 min)

### For Participants
1. Take notes
2. Ask questions
3. Try attacks safely
4. Share findings
5. Practice regularly

### Common Issues

**Issue**: Bandit not finding issues
**Solution**: Check you're in the right directory

**Issue**: Server won't start
**Solution**: Check dependencies installed

**Issue**: Can't fix vulnerability
**Solution**: Review secure examples in api.py

---

## ✅ Workshop Checklist

### Before Workshop
- [ ] Install Python 3.9+
- [ ] Clone repository
- [ ] Install dependencies
- [ ] Test server starts
- [ ] Review documentation

### During Workshop
- [ ] Complete all exercises
- [ ] Take notes
- [ ] Ask questions
- [ ] Share findings
- [ ] Help others

### After Workshop
- [ ] Review materials
- [ ] Practice fixes
- [ ] Integrate SAST
- [ ] Share knowledge
- [ ] Continue learning

---

## 🎉 Conclusion

This workshop provides hands-on experience with:
- Real vulnerability examples
- Industry-standard SAST tools
- Practical remediation techniques
- Best practices integration

**Remember**: Security is a journey, not a destination!

---

**Workshop Contact**: KBTG Security Team  
**Duration**: 2-3 hours  
**Next Steps**: Integrate SAST into your projects!

*"Secure code is not an accident, it's a practice!"* 🔒