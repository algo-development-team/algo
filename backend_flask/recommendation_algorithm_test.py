from recommendation_algorithm import get_one_full_day
from pprint import pprint

def sep():
  print('----------------------------------------------------------------')

time_range1 = '16:00-23:00'
time_range2 = '23:00-7:00'
time_range3 = '1:00-09:00'
time_range4 = '09:00-16:00'
time_ranges = [time_range1, time_range2, time_range3, time_range4]

full_days = [get_one_full_day(time_range) for time_range in time_ranges]

sep()
print('Tested Functions:')
print('get_one_full_day')
sep()
sep()
print('Get One Full Day:')
for i in range(len(full_days)):
  print(f'full day {i}:')
  print(time_ranges[i])
  print(full_days[i])
sep()
