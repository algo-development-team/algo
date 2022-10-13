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

elif ranking_type == 1:
  rankings = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] * 2
  rankings.extend([0, 1, 2, 3])

  user.urgent_rankings_ww = [ranking + 10 for ranking in rankings]
  user.deep_rankings_ww = [ranking + 20 for ranking in rankings]
  user.shallow_rankings_ww = [ranking + 30 for ranking in rankings]
  user.urgent_rankings_pw = [ranking + 40 for ranking in rankings]
  user.deep_rankings_pw = [ranking + 50 for ranking in rankings]
  user.shallow_rankings_pw = [ranking + 60 for ranking in rankings]
  user.urgent_rankings_pnw = [ranking + 70 for ranking in rankings]
  user.deep_rankings_pnw = [ranking + 80 for ranking in rankings]
  user.shallow_rankings_pnw = [ranking + 90 for ranking in rankings]
  db.session.commit()