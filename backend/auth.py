from functools import wraps
from flask import request
from flask_jwt_extended import jwt_required, get_jwt, create_access_token, decode_token
from models import User


# ========token geenreator

def generate_token(user_id, username, role):
    additional_claims = {
        "username": username,
        "role": role
    }
    # identity is typically set to the unique user ID string/integer
    return create_access_token(identity=str(user_id), additional_claims=additional_claims)

#========================================custom decorators===================================


def admin_required(f):
    @wraps(f)
    @jwt_required()  # Ensures a valid JWT exists first
    def decorated(*args, **kwargs):
        claims = get_jwt()  # Read data directly out of the verified token
        if claims.get("role") != 'admin':
            return {"status": "error", "message": "Forbidden. You are not Admin"}, 403
        return f(*args, **kwargs)
    return decorated


def company_required(f):
    @wraps(f)
    @jwt_required()
    def decorated(*args, **kwargs):
        claims = get_jwt()
        if claims.get("role") != 'company':
            return {"status": "error", "message": "Forbidden. Company Person Required"}, 403
        return f(*args, **kwargs)
    return decorated


def student_required(f):
    @wraps(f)
    @jwt_required()
    def decorated(*args, **kwargs):
        claims = get_jwt()
        if claims.get("role") != 'student':
            return {"status": "error", "message": "Forbidden. Students Access Only"}, 403
        return f(*args, **kwargs)
    return decorated