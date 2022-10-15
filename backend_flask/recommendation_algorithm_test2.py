from recommendation_algorithm import get_one_full_day, divide_time_ranges_into_fifteen_minute_groups, get_task_type_index, get_task_type
from datetime import datetime
from pprint import pprint

def sep():
  print('----------------------------------------------------------------')

time_range1 = '16:00-23:00'
time_range2 = '23:00-7:00'
time_range3 = '1:00-9:00'
time_range4 = '9:00-16:00'
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

time_ranges_group1 = [
  (datetime(2022, 10, 12, 12, 0), datetime(2022, 10, 12, 12, 15)),
  (datetime(2022, 10, 12, 12, 30), datetime(2022, 10, 12, 12, 45)),
  (datetime(2022, 10, 12, 14, 0), datetime(2022, 10, 12, 14, 15))
]
time_ranges_group2 = [
  (datetime(2022, 10, 12, 11, 45), datetime(2022, 10, 12, 12, 0)),
  (datetime(2022, 10, 12, 12, 15), datetime(2022, 10, 12, 12, 30)),
  (datetime(2022, 10, 12, 13, 0), datetime(2022, 10, 12, 13, 15))
]

priorities = [1, 2, 3]
day_diffs = [0, 1, 2, 7, 14]
time_lengths = [1, 2, 4, 8]
task_types = []
for priority in priorities:
  for day_diff in day_diffs:
    for time_length in time_lengths:
      task_types.append({
          'task_type': get_task_type(get_task_type_index(priority, day_diff, time_length)),
          'priority': priority,
          'day_diff': day_diff,
          'time_length': time_length
        })


sep()
print('Tested Functions:')
print('get_one_full_day')
print('divide_time_ranges_into_fifteen_minute_ranges')
print('get_task_type_index')
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
sep()
# uncomment to see the output of this function
# print('Get Task Type Index:')
# for task_type in task_types:
#   pprint(task_type)
sep()
