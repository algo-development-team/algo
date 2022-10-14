from recommendation_algorithm import get_tasks_with_highest_relative_priority
from models import User
from pprint import pprint

def sep():
  print('----------------------------------------------------------------')

print('Enter the user\'s email address:')
email = input()
user = User.query.filter_by(email=email).first()

allocatable_tasks_time_ranges = get_tasks_with_highest_relative_priority(user.id)

sep()
print('Allocatable Tasks Time Ranges:')
pprint(allocatable_tasks_time_ranges)
sep()