from app import db 
from models_test_data import user1, user2, user3, workspace1, workspace2, workspace3, category1, category2, category3, task1, task2, task3

# remove all previous data from the database
db.drop_all()
db.session.commit()

# initialize the database
db.create_all()

# input all of models_test_data into the database
db.session.add(user1)
db.session.add(user2)
db.session.add(user3)
db.session.commit()

db.session.add(workspace1)
db.session.add(workspace2)
db.session.add(workspace3)
db.session.commit()

db.session.add(category1)
db.session.add(category2)
db.session.add(category3)
db.session.commit()

db.session.add(task1)
db.session.add(task2)
db.session.add(task3)
db.session.commit()
