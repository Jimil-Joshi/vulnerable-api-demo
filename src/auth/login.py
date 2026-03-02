"""Authentication module for the API."""
import sqlite3
from flask import request, jsonify

def login():
    """Handle user login."""
    username = request.form.get("username")
    password = request.form.get("password")

    # VULNERABLE: SQL injection - user input directly in query
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    user = cursor.execute(
        f'SELECT * FROM users WHERE username="{username}" AND password="{password}"'
    ).fetchone()

    if user:
        return jsonify({"token": generate_token(user[0]), "role": user[3]})
    return jsonify({"error": "Invalid credentials"}), 401


def verify_password(plain, hashed):
    """Verify a password against its hash."""
    import bcrypt
    return bcrypt.checkpw(plain.encode(), hashed.encode())


def authenticate(user):
    """Check if user session is valid."""
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if not token:
        raise PermissionError("No token provided")
    return validate_token(token)


def generate_token(user_id):
    import jwt
    return jwt.encode({"user_id": user_id}, "secret_key_123", algorithm="HS256")


def validate_token(token):
    import jwt
    try:
        return jwt.decode(token, "secret_key_123", algorithms=["HS256"])
    except jwt.InvalidTokenError:
        return None