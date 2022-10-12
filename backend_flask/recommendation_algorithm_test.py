from recommendation_algorithm import get_one_full_day, divide_time_ranges_into_fifteen_minute_groups
from datetime import datetime
from pprint import pprint

def sep():
  print('----------------------------------------------------------------')

time_range1 = '16:00-23:00'
time_range2 = '23:00-7:00'
time_range3 = '1:00-09:00'
time_range4 = '09:00-16:00'
time_ranges = [time_range1, time_range2, time_range3, time_range4]

full_days = [get_one_full_day(time_range) for time_range in time_ranges]

# CONTINUE FROM HERE
start_time1 = datetime(2022, 10, 12, 12, 0)
end_time1 = datetime(2022, 10, 12, 12, 15)
start_time2 = datetime(2022, 10, 12, 12, 0)
end_time2 = datetime(2022, 10, 12, 13, 15)
start_time3 = datetime(2022, 10, 12, 23, 45)
end_time3 = datetime(2022, 10, 13, 0, 15)
time_ranges_dt = [(start_time1, end_time1), (start_time2, end_time2), (start_time3, end_time3)]
fifteen_minute_groups = divide_time_ranges_into_fifteen_minute_groups(time_ranges_dt)

sep()
print('Tested Functions:')
print('get_one_full_day')
print('divide_time_ranges_into_fifteen_minute_ranges')
sep()
sep()
print('Get One Full Day:')
for i in range(len(full_days)):
  print(f'full day {i}:')
  print(time_ranges[i])
  print(full_days[i])
sep()
sep()
print('Divide Time Ranges Into Fifteen Minute Ranges:')
pprint(fifteen_minute_groups)
sep()
