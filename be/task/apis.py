from flask import Blueprint, request, jsonify
from auth.utils import user_required
from db import db
from task.models import Task, TaskStatus, TaskType
from datetime import datetime, timedelta
import jwt, os
import pytz

task_blueprint = Blueprint('task', __name__)
@task_blueprint.route('/create', methods=['POST'])
@user_required
def create_task(user): 
    try:
        user_id = user.id
        task_name = request.json.get('name')

        jakarta_tz = pytz.timezone('Asia/Jakarta')
        completion_date = datetime.now(jakarta_tz).replace(microsecond=0)

        task = Task(
            user_id=user_id,
            type=request.json.get('type', TaskType.low.value),
            status=request.json.get('status', TaskStatus.pending.value),
            name=task_name,
            date=completion_date
        )

        db.session.add(task)
        db.session.commit()

        return jsonify({"task": task.to_dict()}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@task_blueprint.route('/<int:task_id>', methods=['PUT'])
@user_required
def update_task(user, task_id):  
    try:
        task = Task.query.get(task_id)
        if not task:
            return jsonify({"error": "Task not found"}), 404

        allowed_fields = ['type', 'status', 'name']
        update_data = request.json

        for field in allowed_fields:
            if field in update_data:
                setattr(task, field, update_data[field])

        db.session.commit()

        return jsonify({"task": task.to_dict()}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@task_blueprint.route('/<int:id>', methods=['GET'])
@user_required
def get_task(user, id):
    try:
        task = Task.query.get(id)
        if not task:
            return jsonify({"error": "Task not found"}), 404

        return jsonify({"task": task.to_dict()}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# @task_blueprint.route('/', methods=['GET'])
# @user_required
# def get_tasks():
#     try:
#         type_param = request.args.get('type')
#         day = request.args.get('day')
#         user_id = request.json.get('user_id')

#         min_date, max_date = None, None
#         if day == 'today':
#             min_date = datetime.now().strftime('%Y-%m-%d')
#             max_date = datetime.now().strftime('%Y-%m-%d')
#         elif day == 'seven':
#             min_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
#             max_date = datetime.now().strftime('%Y-%m-%d')
#         elif day == 'thirty':
#             min_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
#             max_date = datetime.now().strftime('%Y-%m-%d')

#         tasks = Task.query.filter(Task.user_id == user_id)
#         if type_param:
#             tasks = tasks.filter(Task.type == type_param)
#         if day:
#             tasks = tasks.filter(Task.date >= min_date, Task.date <= max_date)

#         tasks_list = [task.to_dict() for task in tasks]

#         return jsonify({"tasks": tasks_list}), 201
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

@task_blueprint.route('/<int:id>', methods=['DELETE'])
@user_required
def delete_task(user, id):
    try:
        task = Task.query.get(id)
        if not task:
            return jsonify({"error": "Task not found"}), 404

        db.session.delete(task)
        db.session.commit()

        return jsonify({"message": "Task deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
