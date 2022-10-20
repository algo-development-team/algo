from app import db
from models import User
from pprint import pprint

print('Enter the user\'s email address:')
email = input()
user = User.query.filter_by(email=email).first()

rankings = user.get_rankings() 

print('Rankings:')
for key in list(rankings.keys()):
  print(key + ':')
  print(rankings[key])
