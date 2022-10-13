from app import db
from models import User

print('Enter the user\'s email address:')
email = input()
user = User.query.filter_by(email=email).first()
user.checklist = [1, 2, 3]
db.session.commit()