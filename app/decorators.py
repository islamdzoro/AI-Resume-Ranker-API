# utils/auth.py
from functools import wraps
from flask import request, jsonify
from .models import User  # adjust import to your structure

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')

        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error": "Missing or invalid Authorization header."}), 401

        token = auth_header.split("Bearer ")[1].strip()

        user = User.query.filter_by(api_key=token).first()
        if not user:
            return jsonify({"error": "Invalid or revoked API key."}), 403

        request.user = user  # attach user to request for downstream use
        return f(*args, **kwargs)
    return decorated_function
