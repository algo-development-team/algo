from flask import Blueprint, request, jsonify

bp = Blueprint('/api/schedule', __name__, url_prefix='/api/schedule')

# STOPPED HERE
# ADD ROUTE FOR CREATING DAILY SCHEDULE

@bp.route('/daily', methods=['POST'])
def create_daily_calendar_schedule_and_checklist():
  from models import User
  from calendar_schedule import add_task_time_blocks_to_calendar_and_add_task_ids_to_checklist

  data = request.get_json()

  user = User.query.filter_by(email=data['email']).first()
  if user is None:
    return 'User Not Found', 404

  try:
    add_task_time_blocks_to_calendar_and_add_task_ids_to_checklist(user.id)
    pass
  except Exception as e:
    return str(e), 500

  return { 'checklist': user.checklist }

  
  