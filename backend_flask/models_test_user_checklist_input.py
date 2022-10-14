from app import db
from models import User

print('Enter the user\'s email address:')
email = input()
print('Enter the task ids that will go into the checklist, seperated by commas: ex: 1,2,3,...,n')
task_ids_separated_by_commas = input()
user = User.query.filter_by(email=email).first()
user.checklist = task_ids_separated_by_commas.split(',')
db.session.commit()