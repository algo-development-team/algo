from app import db
from models import User

print('Enter the user\'s email address:')
email = input()
user = User.query.filter_by(email=email).first()

print('Enter the input type: 0 for checklist, 1 for work_time_range, 2 for sleep_time_range, 3 for work_days')
input_type = int(input())

if input_type == 0:
  print('Enter the task ids that will go into the checklist, seperated by commas: ex: 1,2,3,...,n')
  task_ids_separated_by_commas = input()
  user.checklist = [int(task_id) for task_id in task_ids_separated_by_commas.split(',') if task_id != '']
  db.session.commit()

if input_type == 1:
  print('Enter the work time range: ex: 9:00-17:00')
  work_time_range = input()
  user.work_time_range = work_time_range
  db.session.commit()

if input_type == 2:
  print('Enter the sleep time range: ex: 23:00-7:00')
  sleep_time_range = input()
  user.sleep_time_range = sleep_time_range
  db.session.commit()

if input_type == 3:
  print('Enter the work days: ex: 0,1,1,1,1,1,0')
  work_days = input()
  user.work_days = [bool(int(work_day)) for work_day in work_days.split(',') if work_day != '']
  db.session.commit()