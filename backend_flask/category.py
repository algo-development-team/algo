from flask import Blueprint, request, jsonify

bp = Blueprint('/api/category', __name__, url_prefix='/api/category')

@bp.route('/<id>', methods=['GET'])
def get_category(id):
  from models import Category

  category = Category.query.get(id)
  if category is None:
    return 'Category Not Found', 404
  
  return jsonify(category.serialize())

@bp.route('/', methods=['POST'])
def create_category():
  from app import db
  from models import Category

  data = request.get_json()

  category = Category(
    name=data['name'],
    workspace_id=data['workspace_id'],
  )

  db.session.add(category)
  db.session.commit()

  return 'Category Created'

@bp.route('/<id>', methods=['DELETE'])
def delete_category(id):
  from app import db
  from models import User, Category

  category = Category.query.get(id)
  if category is None:
    return 'Category Not Found', 404
  
  # remove task id from the user's checklist if it is contained within the user's checklist
  tasks = category.get_tasks()
  for task in tasks:
    if task.user_id is not None:
      user = User.query.get(task.user_id)
      checklist = user.get_checklist()
      if task.id in checklist:
        user.checklist = [task_id for task_id in checklist if task_id != task.id]
        db.session.commit()
  
  db.session.delete(category)
  db.session.commit()

  return 'Category Deleted'

@bp.route('/<id>/update-name', methods=['PATCH'])
def update_name_category(id):
  from app import db
  from models import Category

  data = request.get_json()

  category = Category.query.get(id)
  if category is None:
    return 'Category Not Found', 404

  category.name = data['name']
  db.session.commit()

  return 'Category Name Updated'