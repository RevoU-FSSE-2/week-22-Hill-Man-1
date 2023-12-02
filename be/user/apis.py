from flask import Blueprint, request, jsonify
from auth.utils import admin_required
from task.models import Task
from db import db
from user.models import User, UserRole, UserStatus

user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/users', methods=['GET'])
@admin_required
def get_users(user):
    try:
        users = User.query.all()
        users_list = [user.to_dict() for user in users]
        return jsonify({"users": users_list}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_blueprint.route('/users/<int:id>', methods=['PUT'])
@admin_required
def update_user(user, id):  # Add the user parameter
    try:
        user_to_update = User.query.get(id)
        if not user_to_update:
            return jsonify({"error": "User not found"}), 404
    
        update_data = request.json

        if 'role' in update_data:
            user_to_update.update_role(update_data['role'])

        if 'status' in update_data:
            user_to_update.update_status(update_data['status'])

        db.session.commit()

        return jsonify({"user": user_to_update.to_dict()}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_blueprint.route('/users/<int:id>', methods=['GET'])
@admin_required
def get_user(user, id):  # Add the user parameter
    try:
        user_to_get = User.query.get(id)
        if not user_to_get:
            return jsonify({"error": "User not found"}), 404

        return jsonify({"user": user_to_get.to_dict()}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_blueprint.route('/users/<int:id>', methods=['DELETE'])
@admin_required
def delete_user(user, id):
    try:
        user_to_delete = User.query.get(id)
        tasks_to_delete = Task.query.filter_by(user_id=id).delete()

        if not user_to_delete:
            return jsonify({"error": "User not found"}), 404
        
        db.session.delete(user_to_delete)
        db.session.commit()

        return jsonify({"message": "User deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # try:
    #     user_to_delete = User.query.get(id)
    #     if not user_to_delete:
    #         return jsonify({"error": "User not found"}), 404

    #     # Set user_id to None for associated tasks
    #     Task.query.filter_by(user_id=id).update({"user_id": None})

    #     db.session.delete(user_to_delete)
    #     db.session.commit()

    #     return jsonify({"message": "User deleted successfully"}), 204
    # except Exception as e:
    #     return jsonify({"error": str(e)}), 500
    
    