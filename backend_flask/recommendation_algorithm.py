from models import WorkspaceType, Priority, TimeLength
from user_calendar_data import get_work_and_personal_time_ranges, parse_user_time_range, end_time_round
from datetime import datetime, timedelta
from copy import deepcopy
from pprint import pprint

# helper function
def get_priority_value(PRIORITY):
  if PRIORITY == Priority.LOW:
    return 1
  elif PRIORITY == Priority.AVERAGE:
    return 2
  elif PRIORITY == Priority.HIGH:
    return 3

# helper function
def get_time_length_value(TIME_LENGTH):
  if TIME_LENGTH == TimeLength.FIFTEEN_MIN:
    return 15
  elif TIME_LENGTH == TimeLength.THIRTY_MIN:
    return 30
  elif TIME_LENGTH == TimeLength.ONE_HOUR:
    return 60
  elif TIME_LENGTH == TimeLength.TWO_HOURS:
    return 120
  elif TIME_LENGTH == TimeLength.FOUR_HOURS:
    return 240
  elif TIME_LENGTH == TimeLength.EIGHT_HOURS:
    return 480

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
  if sleep_start <= now < sleep_end:
    return (sleep_end, sleep_start + timedelta(days=1))
  else:
    now = end_time_round(now)
    return (now, sleep_start + timedelta(days=1))

def seperate_work_and_personal_tasks(tasks):
  work_and_personal_tasks = { 'work': [], 'personal': [] }
  for task in tasks:
    workspace_type = task.category.workspace.workspace_type
    if workspace_type == WorkspaceType.WORK:
      work_and_personal_tasks['work'].append(task)
    elif workspace_type == WorkspaceType.PERSONAL:
      work_and_personal_tasks['personal'].append(task)
  return work_and_personal_tasks

def get_relatve_priority_rankings(
  work_and_personal_time_ranges,
  work_days,
  urgent_rankings_ww,
  shallow_rankings_ww,
  deep_rankings_ww,
  urgent_rankings_pw,
  shallow_rankings_pw,
  deep_rankings_pw,
  urgent_rankings_pnw,
  shallow_rankings_pnw,
  deep_rankings_pnw
):
  pass

def get_tasks_with_highest_relative_priority(id):
  from models import User
  user = User.query.get(id)
  (sleep_end_today_or_now, sleep_start_tomorrow) = get_one_full_day(user.sleep_time_range)
  work_and_personal_time_ranges = get_work_and_personal_time_ranges(id, sleep_end_today_or_now, sleep_start_tomorrow, user.work_time_range, user.sleep_time_range)
  # DEBUG (work_and_personal_time_ranges_copy used for debugging only)
  # work_and_personal_time_ranges_copy = deepcopy(work_and_personal_time_ranges)
  # DEBUG
  print('work_and_personal_time_ranges:')
  pprint(work_and_personal_time_ranges)
  
  work_days = user.work_days[:]
  urgent_rankings_ww = user.urgent_rankings_ww[:]
  deep_rankings_ww = user.deep_rankings_ww[:]
  shallow_rankings_ww = user.shallow_rankings_ww[:]
  urgent_rankings_pw = user.urgent_rankings_pw[:]
  deep_rankings_pw = user.deep_rankings_pw[:]
  shallow_rankings_pw = user.shallow_rankings_pw[:]
  urgent_rankings_pnw = user.urgent_rankings_pnw[:]
  deep_rankings_pnw = user.deep_rankings_pnw[:]
  shallow_rankings_pnw = user.shallow_rankings_pnw[:]
  tasks = user.tasks[:]
  
  work_and_personal_tasks = seperate_work_and_personal_tasks(tasks)
  # DEBUG
  print('work_and_personal_tasks:')
  pprint(work_and_personal_tasks)

  # DEBUG
  print('rankings:')
  print(urgent_rankings_ww)
  print(deep_rankings_ww)
  print(shallow_rankings_ww)
  print(urgent_rankings_pw)
  print(deep_rankings_pw)
  print(shallow_rankings_pw)
  print(urgent_rankings_pnw)
  print(deep_rankings_pnw)
  print(shallow_rankings_pnw)

  relative_priority_rankings = get_relatve_priority_rankings(
    work_and_personal_time_ranges=work_and_personal_time_ranges,
    work_days=work_days,
    urgent_rankings_ww=urgent_rankings_ww,
    shallow_rankings_ww=shallow_rankings_ww,
    deep_rankings_ww=deep_rankings_ww,
    urgent_rankings_pw=urgent_rankings_pw,
    shallow_rankings_pw=shallow_rankings_pw,
    deep_rankings_pw=deep_rankings_pw,
    urgent_rankings_pnw=urgent_rankings_pnw,
    shallow_rankings_pnw=shallow_rankings_pnw,
    deep_rankings_pnw=deep_rankings_pnw,
  )

# TEST
def test():
  get_tasks_with_highest_relative_priority(4)

test()