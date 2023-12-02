from flask import Blueprint, Response, request, jsonify
from common.bcrypt import bcrypt
from user.models import User, UserRole, UserStatus
from datetime import datetime, timedelta
from flask_cors import cross_origin
from db import db
import jwt
import os

auth_blp = Blueprint("auth", __name__)

@auth_blp.route('/register', methods=['POST'])
@cross_origin(supports_credentials=True)
def register():
    if request.headers['Content-Type'] == 'application/json':
        data = request.get_json()

        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role')

        user = User.query.filter_by(email=email).first()
        if user:
            return jsonify({
                "error": "Email already in use. Please choose a different email.",
            }), 400

        hash_password = bcrypt.generate_password_hash(password).decode("utf-8")

        new_user = User(name=name, email=email, password=hash_password, role=role)
        db.session.add(new_user)
        db.session.commit()

        role_str = new_user.role.value if new_user.role else None

        return jsonify({
            "id": new_user.id,
            "name": new_user.name,
            "email": new_user.email,
            "role": role_str
        })

    return jsonify({"error": "Invalid Content-Type header"}), 400
@auth_blp.route("/login", methods=['POST'])
@cross_origin(supports_credentials=True)
def login():
    data = request.get_json()
    print("Received data:", data)

    email = data.get('email')
    password = data.get('password')
    role = data.get('role')

    user = User.query.filter_by(email=email).first()
    if not user:
        return {"error": "Email or Password Invalid"}, 400

    valid_password = bcrypt.check_password_hash(user.password, password)
    if not valid_password:
        return {"error": "Email or password is not valid"}, 400

    if user.status == UserStatus.inactive:
        return {"error": "Invalid Status"}, 400

    if not role or UserRole(role) != user.role:
        return {"error": "Invalid Role"}, 400

    payload = {
        "user_id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role.value if user.role else None,
        "exp": datetime.utcnow() + timedelta(minutes=5),
    }
    token = jwt.encode(payload, os.getenv("SECRET_KEY"), algorithm="HS256")

    return jsonify({
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "token": token,
        "role": payload["role"],
    })

