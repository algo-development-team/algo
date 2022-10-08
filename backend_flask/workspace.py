from flask import Blueprint, request, jsonify

bp = Blueprint('/api/workspace', __name__, url_prefix='/api/workspace')

@bp.route('/<id>', methods=['GET'])
def get_workspace(id):
  from models import Workspace

  workspace = Workspace.query.get(id)
  if workspace is None:
    return 'Workspace Not Found', 404
  
  return jsonify(workspace.serialize())

@bp.route('/', methods=['POST'])
def create_workspace():
  from main import db
  from models import Workspace, get_workspace_type

  data = request.get_json()

  workspace_type = get_workspace_type(
    workspace_type=data['workspace_type']
  )

  workspace = Workspace(
    name=data['name'],
    workspace_type=workspace_type,
    members=data['members'],
    admins=data['admins'],
  )

  db.session.add(workspace)
  db.session.commit()

  return 'Workspace Created'

@bp.route('/<id>', methods=['DELETE'])
def delete_workspace(id):
  from main import db
  from models import Workspace

  workspace = Workspace.query.get(id)
  if workspace is None:
    return 'Workspace Not Found', 404

  db.session.delete(workspace)
  db.session.commit()

  return 'Workspace Deleted'

@bp.route('/<id>/update-name', methods=['PATCH'])
def update_name_workspace(id):
  from main import db
  from models import Workspace

  data = request.get_json()

  workspace = Workspace.query.get(id)
  if workspace is None:
    return 'Workspace Not Found', 404

  else:
    workspace.name = data['name']
    db.session.commit()

    return 'Workspace Name Updated'

@bp.route('/<id>/update-members', methods=['PATCH'])
def update_members_workspace(id):
  from main import db
  from models import Workspace

  data = request.get_json()

  workspace = Workspace.query.get(id)
  if workspace is None:
    return 'Workspace Not Found', 404

  else:
    workspace.members = data['members']
    db.session.commit()

    return 'Workspace Members Updated'

@bp.route('/<id>/update-admins', methods=['PATCH'])
def update_admins_workspace(id):
  from main import db
  from models import Workspace

  data = request.get_json()

  workspace = Workspace.query.get(id)
  if workspace is None:
    return 'Workspace Not Found', 404

  else:
    workspace.admins = data['admins']
    db.session.commit()

    return 'Workspace Admins Updated'

@bp.route('/<id>/update-workspace-type', methods=['PATCH'])
def update_workspace_type_workspace(id):
  from main import db
  from models import Workspace, get_workspace_type

  data = request.get_json()

  workspace = Workspace.query.get(id)
  if workspace is None:
    return 'Workspace Not Found', 404

  else:
    workspace_type = get_workspace_type(
      workspace_type=data['workspace_type']
    )
    workspace.workspace_type = workspace_type
    db.session.commit()

    return 'Workspace Type Updated'