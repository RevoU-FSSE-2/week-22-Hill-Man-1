import os
from functools import wraps
from flask import request, jsonify
import jwt
from user.models import UserRole, User

def user_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        token_header = request.headers.get('Authorization')
        if not token_header:
            return {"error": "Token is not valid"}, 401

        try:
            token = token_header.split(" ")[1]
            decoded_token = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms="HS256")
            user_id = decoded_token.get("user_id")
            if user_id:
                user = User.query.get(user_id)
                if user:
                    return fn(user, *args, **kwargs)
                else:
                    return {"error": "User not found"}, 404
            else:
                return {"error": "User access is required"}, 403
        except jwt.ExpiredSignatureError:
            return {"error": "Token has expired"}, 401
        except jwt.InvalidTokenError:
            return {"error": "Token is not valid"}, 401

    return wrapper

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        token_header = request.headers.get('Authorization')
        if not token_header:
            return {"error": "Token is not valid"}, 401

        try:
            token = token_header.split(" ")[1]
            decoded_token = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms="HS256")
            user_id = decoded_token.get("user_id")
            user_role = decoded_token.get("role")
            if user_role == UserRole.admin.value:
                user = User.query.get(user_id)
                if user and user.role == UserRole.admin:
                    return fn(user, *args, **kwargs)
                else:
                    return {"error": "Admin not found"}, 404
            else:
                return {"error": "Admin access is required"}, 403
        except jwt.ExpiredSignatureError:
            return {"error": "Token has expired"}, 401
        except jwt.InvalidTokenError:
            return {"error": "Token is not valid"}, 401

    return wrapper
