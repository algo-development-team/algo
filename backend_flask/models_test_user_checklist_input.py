from app import db
from models import User

user1 = User.query.get(1)
user1.checklist = [1, 2, 3]
db.session.commit()