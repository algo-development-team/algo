from app import db
from models import Task
from datetime import timedelta

print('Enter the number of days shifted:')
days_shifted = int(input())

tasks = Task.query.all()

for task in tasks:
  task.deadline = task.deadline + timedelta(days=days_shifted)
  db.session.commit()