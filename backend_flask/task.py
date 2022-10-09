from flask import Blueprint, request, jsonify
from datetime import datetime

bp = Blueprint('/api/task', __name__, url_prefix='/api/task')

@bp.route('/<id>', methods=['GET'])
def get_task(id):
  from models import Task

  task = Task.query.get(id)
  if task is None:
    return 'Task Not Found', 404
  
  return jsonify(task.serialize())

@bp.route('/', methods=['POST'])
def create_task():
  from app import db
  from models import Task, get_priority, get_time_length

  data = request.get_json()

  priority = get_priority(data['priority'])
  time_length = get_time_length(data['time_length'])
  deadline = None
  user_id = None

  if data['deadline'] is not None:
    deadline = datetime.strptime(data['deadline'], '%Y-%m-%d')

  if data['user_id'] is not None:
    user_id = data['user_id']

  task = Task(
    title=data['title'],
    description=data['description'],
    priority=priority,
    time_length=time_length,
    deadline=deadline,
    user_id=user_id,
    category_id=data['category_id'],
  )

  db.session.add(task)
  db.session.commit()

  return 'Task Created'

@bp.route('/<id>', methods=['DELETE'])
def delete_task(id):
  from app import db
  from models import Task

  task = Task.query.get(id)
  if task is None:
    return 'Task Not Found', 404

  db.session.delete(task)
  db.session.commit()

  return 'Task Deleted'

@bp.route('/<id>/update', methods=['PATCH'])
def update_task(id):
  from app import db
  from models import Task, get_priority, get_time_length

  data = request.get_json()

  task = Task.query.get(id)
  if task is None:
    return 'Task Not Found', 404

  task.title = data['title']
  task.description = data['description']
  task.priority = get_priority(data['priority'])
  task.time_length = get_time_length(data['time_length'])
  task.deadline = datetime.strptime(data['deadline'], '%Y-%m-%d')
  task.user_id = data['user_id']

  db.session.commit()

  return 'Task Updated'

@bp.route('/<id>/update-completed', methods=['PATCH'])
def update_completed_task(id):
  from app import db
  from models import Task

  task = Task.query.get(id)
  if task is None:
    return 'Task Not Found', 404

  task.completed = True
  db.session.commit()

  return 'Task Completed Updated'

@bp.route('/<id>/update-undo-completed', methods=['PATCH'])
def update_undo_completed_task(id):
  from app import db
  from models import Task

  task = Task.query.get(id)
  if task is None:
    return 'Task Not Found', 404

  task.completed = False
  db.session.commit()

  return 'Task Undo Completed Updated'

@bp.route('/<id>/update-category', methods=['PATCH'])
def update_category_task(id):
  from app import db
  from models import Task

  data = request.get_json()

  task = Task.query.get(id)
  if task is None:
    return 'Task Not Found', 404

  task.category_id = data['category_id']
  db.session.commit()

  return 'Task Category Updated'

@bp.route('/<id>/update-user', methods=['PATCH'])
def update_user_task(id):
  from app import db
  from models import Task

  data = request.get_json()

  task = Task.query.get(id)
  if task is None:
    return 'Task Not Found', 404

  task.user_id = data['user_id']
  db.session.commit()

  return 'Task User Updated'