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
    @jwt_required() # Automatically validates token headers, signature, and expiration
    def decorated(current_user, *args, **kwargs):
        if current_user['role'] != 'admin':
            return {"status": "error", "message": "Forbidden. You are not Admin"}, 403
        return f(current_user, *args, **kwargs)
    return decorated


def company_required(f):
    @wraps(f)
    @jwt_required()
    def decorated(current_user, *args, **kwargs):
        if current_user['role'] != 'company':
            return {"status": "error", "message": "Forbidden. Company Person Required"}, 403
        return f(current_user, *args, **kwargs)
    return decorated


def student_required(f):
    """Restricts route access strictly to registered Students"""
    @wraps(f)
    @jwt_required()
    def decorated(current_user, *args, **kwargs):
        if current_user['role'] != 'student':
            return {"status": "error", "message": "Forbidden. Students Access Only"}, 403
        return f(current_user, *args, **kwargs)
    return decorated