"""
Vulnerable API routes - FOR WORKSHOP TRAINING ONLY!
⚠️ WARNING: Contains intentional security vulnerabilities
DO NOT USE IN PRODUCTION!

These endpoints demonstrate common security vulnerabilities
that SAST tools should detect.
"""
from flask import Blueprint, request, jsonify
import sqlite3
import subprocess
import os
import pickle
import base64
import hashlib
import random

vulnerable_bp = Blueprint('vulnerable', __name__)


@vulnerable_bp.route('/search', methods=['GET'])
def search_contacts():
    """
    VULNERABILITY: SQL Injection (CWE-89)
    SAST Detection: Bandit B608, SonarQube S2077
    
    This endpoint is vulnerable to SQL injection attacks
    because it uses string concatenation to build SQL queries.
    """
    search_term = request.args.get('q', '')
    
    # VULNERABLE: Direct string concatenation in SQL query
    conn = sqlite3.connect('data/webscraper.db')
    cursor = conn.cursor()
    
    # Bandit will flag this as B608 (hardcoded SQL string)
    query = f"SELECT * FROM contacts WHERE name LIKE '%{search_term}%'"
    cursor.execute(query)  # SQL Injection vulnerability
    
    results = cursor.fetchall()
    conn.close()
    
    return jsonify({
        'success': True,
        'results': results,
        'query': query  # Exposing query is also a security issue
    })


@vulnerable_bp.route('/backup', methods=['POST'])
def backup_database():
    """
    VULNERABILITY: Command Injection (CWE-78)
    SAST Detection: Bandit B602, B607, SonarQube S4721
    
    This endpoint is vulnerable to command injection
    because it uses shell=True with user input.
    """
    filename = request.json.get('filename', 'backup.db')
    
    # VULNERABLE: Using shell=True with user input
    backup_path = f"/backups/{filename}"
    command = f"cp data/webscraper.db {backup_path}"
    
    # Bandit will flag this as B602 (shell=True) and B607 (partial shell path)
    result = subprocess.call(command, shell=True)
    
    return jsonify({
        'success': True,
        'message': f'Backup created at {backup_path}',
        'command': command  # Exposing command is also a security issue
    })


@vulnerable_bp.route('/execute', methods=['POST'])
def execute_command():
    """
    VULNERABILITY: OS Command Injection (CWE-78)
    SAST Detection: Bandit B605, B607
    
    This endpoint allows arbitrary command execution.
    """
    command = request.json.get('command', 'ls')
    
    # VULNERABLE: Direct execution of user input
    # Bandit will flag this as B605 (start_process_with_a_shell)
    os.system(command)
    
    return jsonify({
        'success': True,
        'message': 'Command executed',
        'command': command
    })


@vulnerable_bp.route('/download', methods=['GET'])
def download_file():
    """
    VULNERABILITY: Path Traversal (CWE-22)
    SAST Detection: SonarQube S5131, Semgrep path-traversal
    
    This endpoint is vulnerable to path traversal attacks
    because it doesn't validate the file path.
    """
    filename = request.args.get('file', '')
    
    # VULNERABLE: No path validation
    # Attacker can use ../../../etc/passwd
    file_path = f"data/{filename}"
    
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        return jsonify({
            'success': True,
            'content': content,
            'path': file_path  # Exposing path is also a security issue
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404


@vulnerable_bp.route('/session/load', methods=['POST'])
def load_session():
    """
    VULNERABILITY: Insecure Deserialization (CWE-502)
    SAST Detection: Bandit B301, SonarQube S5135
    
    This endpoint uses pickle to deserialize untrusted data,
    which can lead to arbitrary code execution.
    """
    session_data = request.json.get('session', '')
    
    try:
        # VULNERABLE: Unpickling untrusted data
        # Bandit will flag this as B301 (pickle usage)
        decoded = base64.b64decode(session_data)
        user_data = pickle.loads(decoded)  # Arbitrary code execution risk
        
        return jsonify({
            'success': True,
            'data': user_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@vulnerable_bp.route('/hash-password', methods=['POST'])
def hash_password():
    """
    VULNERABILITY: Weak Cryptography (CWE-327)
    SAST Detection: Bandit B303, B324, SonarQube S4790
    
    This endpoint uses MD5 for password hashing,
    which is cryptographically broken.
    """
    password = request.json.get('password', '')
    
    # VULNERABLE: MD5 is cryptographically broken
    # Bandit will flag this as B303 (MD5) and B324 (hashlib)
    hashed = hashlib.md5(password.encode()).hexdigest()
    
    return jsonify({
        'success': True,
        'hash': hashed,
        'algorithm': 'md5'  # Exposing algorithm is also a security issue
    })


@vulnerable_bp.route('/generate-token', methods=['GET'])
def generate_token():
    """
    VULNERABILITY: Weak Random Number Generator (CWE-338)
    SAST Detection: Bandit B311, SonarQube S2245
    
    This endpoint uses random module for security-sensitive operations,
    which is not cryptographically secure.
    """
    # VULNERABLE: random is not cryptographically secure
    # Bandit will flag this as B311 (random usage)
    token = str(random.randint(100000, 999999))
    
    return jsonify({
        'success': True,
        'token': token
    })


@vulnerable_bp.route('/proxy', methods=['GET'])
def proxy_request():
    """
    VULNERABILITY: Server-Side Request Forgery (SSRF) (CWE-918)
    SAST Detection: SonarQube S5144, Semgrep SSRF
    
    This endpoint makes requests to user-supplied URLs
    without validation, allowing SSRF attacks.
    """
    import requests
    
    url = request.args.get('url', '')
    
    # VULNERABLE: No URL validation
    # Attacker can access internal services
    try:
        response = requests.get(url, timeout=5)
        
        return jsonify({
            'success': True,
            'content': response.text[:1000],
            'status': response.status_code,
            'url': url  # Exposing URL is also a security issue
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@vulnerable_bp.route('/eval', methods=['POST'])
def eval_code():
    """
    VULNERABILITY: Code Injection (CWE-94)
    SAST Detection: Bandit B307, SonarQube S1523
    
    This endpoint evaluates user-supplied Python code,
    allowing arbitrary code execution.
    """
    code = request.json.get('code', '')
    
    try:
        # VULNERABLE: eval() with user input
        # Bandit will flag this as B307 (eval usage)
        result = eval(code)
        
        return jsonify({
            'success': True,
            'result': str(result),
            'code': code
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@vulnerable_bp.route('/info', methods=['GET'])
def get_info():
    """
    Information endpoint about vulnerable routes
    """
    return jsonify({
        'warning': '⚠️ These endpoints contain intentional security vulnerabilities',
        'purpose': 'SAST workshop training only',
        'do_not_use': 'DO NOT USE IN PRODUCTION',
        'vulnerabilities': [
            {
                'endpoint': '/vulnerable/search',
                'vulnerability': 'SQL Injection',
                'cwe': 'CWE-89',
                'severity': 'CRITICAL'
            },
            {
                'endpoint': '/vulnerable/backup',
                'vulnerability': 'Command Injection',
                'cwe': 'CWE-78',
                'severity': 'CRITICAL'
            },
            {
                'endpoint': '/vulnerable/execute',
                'vulnerability': 'OS Command Injection',
                'cwe': 'CWE-78',
                'severity': 'CRITICAL'
            },
            {
                'endpoint': '/vulnerable/download',
                'vulnerability': 'Path Traversal',
                'cwe': 'CWE-22',
                'severity': 'HIGH'
            },
            {
                'endpoint': '/vulnerable/session/load',
                'vulnerability': 'Insecure Deserialization',
                'cwe': 'CWE-502',
                'severity': 'CRITICAL'
            },
            {
                'endpoint': '/vulnerable/hash-password',
                'vulnerability': 'Weak Cryptography',
                'cwe': 'CWE-327',
                'severity': 'MEDIUM'
            },
            {
                'endpoint': '/vulnerable/generate-token',
                'vulnerability': 'Weak Random',
                'cwe': 'CWE-338',
                'severity': 'MEDIUM'
            },
            {
                'endpoint': '/vulnerable/proxy',
                'vulnerability': 'SSRF',
                'cwe': 'CWE-918',
                'severity': 'HIGH'
            },
            {
                'endpoint': '/vulnerable/eval',
                'vulnerability': 'Code Injection',
                'cwe': 'CWE-94',
                'severity': 'CRITICAL'
            }
        ]
    })

# Made with Bob
