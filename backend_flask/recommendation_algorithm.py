from user_calendar_data import get_work_and_personal_time_ranges, parse_user_time_range
from datetime import datetime, timedelta

# helper function
# parameter specification:
# sleep_time_range: 'Hour:MM-Hour:MM', where Hour is 'H' or 'HH'
# return value specification:
# (sleep_end, sleep_start) or (now, sleep_start)
# sleep_end, sleep_start, now: datetime.datetime(year, month, day, hour, min)
def get_one_full_day(sleep_time_range):
  parsed_sleep_time_range = parse_user_time_range(sleep_time_range)
  now = datetime.now()
  now = datetime(now.year, now.month, now.day, now.hour, now.minute)
  sleep_end = datetime(now.year, now.month, now.day, parsed_sleep_time_range['end']['hour'], parsed_sleep_time_range['end']['minute'])
  sleep_start = datetime(now.year, now.month, now.day, parsed_sleep_time_range['start']['hour'], parsed_sleep_time_range['start']['minute'])
  if sleep_start > sleep_end:
    sleep_start = sleep_start - timedelta(days=1)
  # convert_minute_only = lambda hour, minute : hour * 60 + minute
  # now_minute = convert_minute_only(now.hour, now.minute)
  # sleep_end_minute = convert_minute_only(sleep_end.hour, sleep_end.minute)
  # if now < sleep_end:
  #   sleep_end -= timedelta(days=1)
  if sleep_start <= now < sleep_end:
    print('between sleep_start and sleep_end')
    return (sleep_end, sleep_start + timedelta(days=1))
  else:
    return (now, sleep_start + timedelta(days=1))

def get_tasks_with_highest_relative_priority(id):
  from models import User
  user = User.query.get(id)
  (sleep_end_today_or_now, sleep_start_tomorrow) = get_one_full_day(user.sleep_time_range)
  work_and_personal_time_ranges = get_work_and_personal_time_ranges(id, sleep_end_today_or_now, sleep_start_tomorrow, user.work_time_range, user.sleep_time_range)

