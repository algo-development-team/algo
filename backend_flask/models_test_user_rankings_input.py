from app import db
from models import User

print('Enter the user\'s email address:')
email = input()
user = User.query.filter_by(email=email).first()

print('Enter the ranking type: 0 for all 50, 1 for 10-99')
ranking_type = int(input())

if ranking_type == 0:
  rankings = [50] * 24

  user.urgent_rankings_ww = rankings
  user.deep_rankings_ww = rankings
  user.shallow_rankings_ww = rankings
  user.urgent_rankings_pw = rankings
  user.deep_rankings_pw = rankings
  user.shallow_rankings_pw = rankings
  user.urgent_rankings_pnw = rankings
  user.deep_rankings_pnw = rankings
  user.shallow_rankings_pnw = rankings
  db.session.commit()