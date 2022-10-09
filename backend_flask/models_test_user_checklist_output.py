from app import db
from models import User

user1 = User.query.get(1)
checklist = user1.checklist[:]
print(checklist)