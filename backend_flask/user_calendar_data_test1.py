from models import User
from user_calendar_data import get_empty_time_ranges, get_dt_fifteen_min_rounded, get_user_events_time_range, get_user_time_zone, get_user_calendar_id_list, separate_periods_time_ranges
from datetime import datetime, timedelta
from pprint import pprint

def sep():
  print('----------------------------------------------------------------')

print('Enter the user\'s email address:')
email = input()
user = User.query.filter_by(email=email).first()
if user is None:
  print('User Not Found')
else:
  # time_now = datetime.now()
  # time_min_seconds_not_rounded = get_dt_fifteen_min_rounded([(time_now, time_now)])[0][1]
  # time_min = datetime(time_min_seconds_not_rounded.year, time_min_seconds_not_rounded.month, time_min_seconds_not_rounded.day, time_min_seconds_not_rounded.hour, time_min_seconds_not_rounded.minute)
  # time_max = time_min + timedelta(days=1)
  # FOR TESTING ONLY
  time_min = datetime(2022, 10, 12, 0, 0)
  time_max = datetime(2022, 10, 13, 0, 0)
  time_ranges = get_dt_fifteen_min_rounded(get_user_events_time_range(user.id, time_min, time_max))
  empty_time_ranges = get_empty_time_ranges(user.id, time_min, time_max)
  work_time_range = '9:00-17:00'
  sleep_time_range = '23:00-7:00'
  work_and_personal_time_ranges = separate_periods_time_ranges(user.id, empty_time_ranges, work_time_range, sleep_time_range)

  sep()
  print('Tested Functions:')
  print('get_empty_time_ranges')
  print('get_dt_fifteen_min_rounded')
  print('get_user_events_time_range')
  print('get_user_time_zone')
  print('get_user_calendar_id_list')
  print('separate_periods_time_ranges')
  sep()
  sep()
  print('User\'s Time Zone: ', get_user_time_zone(user.id))
  sep()
  sep()
  print('User\'s Calendar List:')
  pprint(get_user_calendar_id_list(user.id))
  sep()
  sep()
  for i in range(len(time_ranges)):
    start_time = time_ranges[i][0]
    end_time = time_ranges[i][1]
    print('Event ' + str(i) + ':')
    print('Start Time: ' + str(start_time))
    print('End Time: ' + str(end_time))
  sep()
  sep()
  for i in range(len(empty_time_ranges)):
    start_time = empty_time_ranges[i][0]
    end_time = empty_time_ranges[i][1]
    print('Empty Block ' + str(i) + ':')
    print('Start Time: ' + str(start_time))
    print('End Time: ' + str(end_time))
  sep()
  sep()
  print('Separated Periods Time Ranges:')
  pprint(work_and_personal_time_ranges)
  sep()
