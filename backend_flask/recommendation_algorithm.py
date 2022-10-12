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

# parameter specification:
# time_ranges: (start_time, end_time)[]
# start_time: datetime.datetime(year, month, day, hour, min)
# end_time: datetime.datetime(year, month, day, hour, min)
# condition: minute of start_time and end_time are already rounded to fifteen minutes
# return value specification:
# (start_time, end_time)[][]
def divide_time_ranges_into_fifteen_minute_groups(time_ranges):
  time_ranges_copy = time_ranges[:]
  time_ranges_fifteen_minute_groups = []
  for time_range in time_ranges_copy:
    time_ranges_fifteen_minute_group = []
    start_time = time_range[0]
    end_time = time_range[1]
    while (start_time < end_time):
      time_ranges_fifteen_minute_group.append((start_time, start_time + timedelta(seconds=900)))
      start_time += timedelta(seconds=900)
    time_ranges_fifteen_minute_groups.append(time_ranges_fifteen_minute_group)
  return time_ranges_fifteen_minute_groups

# helper function
# parameter specification:
# time_range_groups: (start_time, end_time)[][]
def get_rankings_for_each_time_range_in_groups(
  time_range_groups,
  work_days,
  rankings
):
  time_range_groups_copy = time_range_groups[:]
  for i in range(len(time_range_groups_copy)):
    for j in range(len(time_range_groups_copy[i])):
      # start_time = time_range_groups_copy[i][j][0]
      pass

# wrapper function for
# divide_time_ranges_into_fifteen_minute_groups
# and
# get_rankings_for_each_time_range_in_groups
def get_work_and_personal_time_ranges_rankings(
  work_and_personal_time_ranges,
  work_days,
  rankings
):
  # work_and_personal_time_ranges_fifteen_minutes = { 
  #   'work': divide_time_ranges_into_fifteen_minute_groups(work_and_personal_time_ranges['work']), 
  #   'personal': divide_time_ranges_into_fifteen_minute_groups(work_and_personal_time_ranges['personal'])
  # }
  work_and_personal_time_ranges_fifteen_minutes = {
    'work': get_rankings_for_each_time_range_in_groups(
      time_range_groups=divide_time_ranges_into_fifteen_minute_groups(work_and_personal_time_ranges['work']),
      work_days=work_days,
      rankings=rankings
    ),
    'personal': get_rankings_for_each_time_range_in_groups(
      time_range_groups=divide_time_ranges_into_fifteen_minute_groups(work_and_personal_time_ranges['personal']),
      work_days=work_days,
      rankings=rankings
    )
  }
  return work_and_personal_time_ranges_fifteen_minutes

def get_tasks_with_highest_relative_priority(id):
  from models import User
  user = User.query.get(id)
  (sleep_end_today_or_now, sleep_start_tomorrow) = get_one_full_day(user.sleep_time_range)
  work_and_personal_time_ranges = get_work_and_personal_time_ranges(id, sleep_end_today_or_now, sleep_start_tomorrow, user.work_time_range, user.sleep_time_range)
  # DEBUG (work_and_personal_time_ranges_copy used for debugging only)
  # work_and_personal_time_ranges_copy = deepcopy(work_and_personal_time_ranges)
  # DEBUG
  # print('work_and_personal_time_ranges:')
  # pprint(work_and_personal_time_ranges)
  
  work_days = user.work_days[:]
  rankings = user.get_rankings()
  tasks = user.tasks[:]
  
  work_and_personal_tasks = seperate_work_and_personal_tasks(tasks)
  # DEBUG
  # print('work_and_personal_tasks:')
  # pprint(work_and_personal_tasks)

  work_and_personal_time_ranges_rankings = get_work_and_personal_time_ranges_rankings(
    work_and_personal_time_ranges=work_and_personal_time_ranges,
    work_days=work_days,
    rankings=rankings
  )

# TEST
def test():
  get_tasks_with_highest_relative_priority(4)

test()