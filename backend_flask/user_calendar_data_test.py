from models import User
from user_calendar_data import get_empty_time_ranges_and_durations, get_dt_fifteen_min_rounded, get_user_events_time_range, get_user_time_zone, get_user_calendar_id_list
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
  time_min = datetime(2022, 10, 11, 0, 0)
  time_max = datetime(2022, 10, 12, 0, 0)
  empty_time_ranges_and_durations = get_empty_time_ranges_and_durations(user.id, time_min, time_max)
  time_ranges = get_dt_fifteen_min_rounded(get_user_events_time_range(user.id, time_min, time_max))
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
  for i in range(len(empty_time_ranges_and_durations)):
    start_time = empty_time_ranges_and_durations[i][0]
    end_time = empty_time_ranges_and_durations[i][1]
    duration = empty_time_ranges_and_durations[i][2]
    hours = duration // 60
    minutes = duration % 60
    print('Empty Block ' + str(i) + ':')
    print('Start Time: ' + str(start_time))
    print('End Time: ' + str(end_time))
    print('Duration: ' + str(hours) + 'h ' + str(minutes) + 'm')
  sep()
