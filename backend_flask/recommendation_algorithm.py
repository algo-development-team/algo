from models import WorkspaceType, Priority, TimeLength, TaskType
from user_calendar_data import get_work_and_personal_time_ranges, parse_user_time_range, end_time_round
from datetime import datetime, timedelta
from copy import deepcopy
from pprint import pprint

# constants
DEFAULT_TASK_TYPE = TaskType.NONE

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
    return 1
  elif TIME_LENGTH == TimeLength.THIRTY_MIN:
    return 2
  elif TIME_LENGTH == TimeLength.ONE_HOUR:
    return 4
  elif TIME_LENGTH == TimeLength.TWO_HOURS:
    return 8
  elif TIME_LENGTH == TimeLength.FOUR_HOURS:
    return 16
  elif TIME_LENGTH == TimeLength.EIGHT_HOURS:
    return 32

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

# parameter specification:
# work_and_personal_time_ranges: { 'work': (start_time, end_time)[], 'personal': (start_time, end_time)[] }
# work_days: bool[7]
# rankings: int[9][24] (rankings from User.get_rankings())
def get_work_and_personal_time_ranges_rankings(
  work_and_personal_time_ranges,
  work_days,
  rankings
):
  work_and_personal_time_ranges_fifteen_minute_groups = {
    'work': divide_time_ranges_into_fifteen_minute_groups(work_and_personal_time_ranges['work']),
    'personal': divide_time_ranges_into_fifteen_minute_groups(work_and_personal_time_ranges['personal']), 
  }

  # work_and_personal_time_ranges_rankings['work' or 'personal'] data structure:
  # { 'time_range': (start_time, end_time), 'rankings': (urgent, deep, shallow) }[][]
  work_and_personal_time_ranges_rankings = { 'work': [], 'personal': [] }

  for work_time_ranges_group in work_and_personal_time_ranges_fifteen_minute_groups['work']:
    time_ranges_rankings_group = []
    for work_time_range in work_time_ranges_group:
      start_time = work_time_range[0]
      hour = start_time.hour
      is_work_day = work_days[int(start_time.date().strftime('%w'))]
      # ww (work-working-day)
      if is_work_day:
        time_ranges_rankings_group.append({
          'time_range': work_time_range,
          'rankings': (
            rankings['urgent_rankings_ww'][hour],
            rankings['deep_rankings_ww'][hour],
            rankings['shallow_rankings_ww'][hour],
          )
        })
      # pnw (personal-non-working-day)
      else:
        time_ranges_rankings_group.append({
          'time_range': work_time_range,
          'rankings': (
            rankings['urgent_rankings_pnw'][hour],
            rankings['deep_rankings_pnw'][hour],
            rankings['shallow_rankings_pnw'][hour],
          )
        })
    work_and_personal_time_ranges_rankings['work'].append(time_ranges_rankings_group)

  for personal_time_ranges_group in work_and_personal_time_ranges_fifteen_minute_groups['personal']:
    time_ranges_rankings_group = []
    for personal_time_range in personal_time_ranges_group:
      start_time = personal_time_range[0]
      hour = start_time.hour
      is_work_day = work_days[int(start_time.date().strftime('%w'))]
      # pw (personal-working-day)
      if is_work_day:
        time_ranges_rankings_group.append({
          'time_range': personal_time_range,
          'rankings': (
            rankings['urgent_rankings_pw'][hour],
            rankings['deep_rankings_pw'][hour],
            rankings['shallow_rankings_pw'][hour],
          )
        })
      # pnw (personal-non-working-day)
      else:
        time_ranges_rankings_group.append({
          'time_range': personal_time_range,
          'rankings': (
            rankings['urgent_rankings_pnw'][hour],
            rankings['deep_rankings_pnw'][hour],
            rankings['shallow_rankings_pnw'][hour],
          )
        })
    work_and_personal_time_ranges_rankings['personal'].append(time_ranges_rankings_group)
      
  return work_and_personal_time_ranges_rankings

# helper function
# parameter specification:
# tasks: Task[]
# return value specification:
# { 'id': int, 'section': int (1-4), 'priority': int (1-3), 'deadline': datetime.datetime(year, month, day, hour, min), 'time_length': int (1, 2, 4, 8), 'time_ranges': [] (later datetime.datetime(year, month, day, hour, min)[]), 'task_type': DEFAULT_TASK_TYPE (later TaskType) }[]
def get_tasks_transformed(tasks):
  tasks_transformed = []
  for task in tasks:
    priority_value = get_priority_value(task.priority)
    total_time_length = get_time_length_value(task.time_length)
    num_sections = total_time_length // 8 if total_time_length % 8 == 0 else (total_time_length // 8) + 1
    for i in range(num_sections):
      task_transformed = {
        'id': task.id,
        'section': i + 1,
        'priority': priority_value,
        'deadline': task.deadline,
        'time_length': total_time_length - (i * 8) if total_time_length - (i * 8) < 8 else 8,
        'time_ranges': [],
        'task_type': DEFAULT_TASK_TYPE,
      }
      tasks_transformed.append(task_transformed)
  return tasks_transformed

# helper function
# parameter specification:
# task_type_index: int (1-3)
# return value specification:
# int (0-2)
def get_task_type_index(task_type):
  if task_type == TaskType.URGENT:
    return 0
  elif task_type == TaskType.DEEP:
    return 1
  elif task_type == TaskType.SHALLOW:
    return 2

# helper function
# parameter specification:
# priority: int (1-3)
# day_diff: int (0-14)
# time_length: int (1, 2, 4, 8)
# return value specification:
# TaskType
def get_task_type(priority, day_diff, time_length):
  # shallow by-default
  if priority == 1:
    return TaskType.SHALLOW
  # deep or shallow
  elif priority == 2:
    # shallow (15 min or 30 min)
    if time_length <= 2:
      return TaskType.SHALLOW
    # deep (1 hour or longer)
    else:
      return TaskType.DEEP
  # urgent or deep by-default
  elif priority == 3:
    # urgent (today, tomorrow, day-after-tomorrow)
    if day_diff <= 2:
      return TaskType.URGENT
    # deep 
    else:
      return TaskType.DEEP

def multiply_parameters_and_values(parameters, values, keys):
  total = 0
  for key in keys:
    total += parameters[key] * values[key]
  return total

# helper function
# parameter specification:
# day_diff: int (0-14)
# return value specification:
# float (0-1)
def get_day_diff_value_transformed(day_diff):
  day_diff_positive = 15 - day_diff
  if day_diff_positive == 15:
    day_diff_positive = 50
  elif day_diff_positive == 14:
    day_diff_positive = 30
  elif day_diff_positive == 13:
    day_diff_positive = 20
  elif day_diff_positive == 12:
    day_diff_positive = 15
  elif day_diff_positive == 11:
    day_diff_positive = 12
  day_diff_value_transformed = day_diff_positive ** 2 / 2500
  return day_diff_value_transformed

# helper function
# parameter specification:
# task: { 'id': int, 'section': int (1-4), 'priority': int (1-3), 'deadline': datetime.datetime(year, month, day, hour, min), 'time_length': int (1, 2, 4, 8), 'time_ranges': datetime.datetime(year, month, day, hour, min)[] }[]
# return value specification:
# task: { 'id': int, 'section': int (1-4), 'priority': int (1-3), 'deadline': datetime.datetime(year, month, day, hour, min), 'time_length': int (1, 2, 4, 8), 'time_ranges': datetime.datetime(year, month, day, hour, min)[] }[]
# tasks already sorted in order of 'id' and 'section'
def combine_sections_time_length(tasks):
  combined_tasks = [deepcopy(task) for task in tasks]

  remaining_time_length = {}
  for task in combined_tasks:
    if task['time_length'] < 8:
      task_id_str = str(task['id'])
      if task_id_str not in remaining_time_length:
        remaining_time_length[task_id_str] = task['time_length']  
      else:
        remaining_time_length[task_id_str] += task['time_length']  
  for i in range(len(combined_tasks)):
    task = combined_tasks[i]
    if task['time_length'] < 8:
      task_id_str = str(task['id'])
      new_time_length = min(remaining_time_length[task_id_str], 8)
      combined_tasks[i]['time_length'] = new_time_length
      remaining_time_length[task_id_str] -= new_time_length

  return combined_tasks

# helper function
# parameter specification:
# task_type1: TaskType
# task_type2: TaskType
# return value specification:
# TaskType
def determine_task_type(task_type1, task_type2):
  def get_task_type_value(task_type):
    if task_type == TaskType.URGENT:
      return 3
    elif task_type == TaskType.DEEP:
      return 2
    elif task_type == TaskType.SHALLOW:
      return 1
    elif task_type == TaskType.NONE:
      return 0
  def get_task_type_from_value(value):
    if value == 3:
      return TaskType.URGENT
    elif value == 2:
      return TaskType.DEEP
    elif value == 1:
      return TaskType.SHALLOW
    elif value == 0:
      return TaskType.NONE
  task_type_higher_value = max(get_task_type_value(task_type1), get_task_type_value(task_type2))
  task_type_higher = get_task_type_from_value(task_type_higher_value)
  return task_type_higher

# helper function
# parameter specification:
# task: { 'id': int, 'section': int (1-4), 'priority': int (1-3), 'deadline': datetime.datetime(year, month, day, hour, min), 'time_length': int (1, 2, 4, 8), 'time_ranges': datetime.datetime(year, month, day, hour, min)[], 'task_type': TaskType }[]
# return value specfication:
# { 'task_id_str': { 'time_ranges': time_ranges[] (time_ranges sorted in sequential order), 'task_type': TaskType } }
def combine_tasks_sections_and_time_ranges_sorted(tasks):
  
  combined_tasks_sections_and_time_ranges_sorted = {}
  for task in tasks:
    task_id_str = str(task['id'])
    if task_id_str not in combined_tasks_sections_and_time_ranges_sorted:
      combined_tasks_sections_and_time_ranges_sorted[task_id_str] = { 
        'time_ranges': task['time_ranges'],
        'task_type': task['task_type']
      }  
    else:
      combined_tasks_sections_and_time_ranges_sorted[task_id_str]['time_ranges'] += task['time_ranges']
      combined_tasks_sections_and_time_ranges_sorted[task_id_str]['task_type'] = determine_task_type(combined_tasks_sections_and_time_ranges_sorted[task_id_str]['task_type'], task['task_type'])

  for task_id_str in combined_tasks_sections_and_time_ranges_sorted:
    combined_tasks_sections_and_time_ranges_sorted[task_id_str]['time_ranges'] = sorted(combined_tasks_sections_and_time_ranges_sorted[task_id_str]['time_ranges'], key=lambda time_range: time_range[0])

  return combined_tasks_sections_and_time_ranges_sorted 

# helper function
# parameter specification:
# { 'task_id_str': { 'time_ranges': time_ranges[] (time_ranges sorted in sequential order), 'task_type': TaskType } }
# return value specfication:
# { 'task_id_str': { 'time_ranges': time_ranges[] (time_ranges sorted in sequential order), 'task_type': TaskType } }
def merge_tasks_time_ranges(tasks):
  merged_tasks = {}
  for task_id_str in tasks:
    merged_time_ranges = []
    for time_range in tasks[task_id_str]['time_ranges']:
      if len(merged_time_ranges) == 0:
        merged_time_ranges.append(time_range)
      else:
        last_entry = merged_time_ranges[len(merged_time_ranges) - 1]
        if time_range[0] == last_entry[1]:
          merged_time_ranges[len(merged_time_ranges) - 1] = (last_entry[0], time_range[1])
        else:
          merged_time_ranges.append(time_range)
    merged_tasks[task_id_str] = {
      'time_ranges': merged_time_ranges,
      'task_type': tasks[task_id_str]['task_type']
    }
  return merged_tasks

# helper function
# parameter specification:
# work_and_personal_time_ranges_rankings: { 'work': time_ranges_groups, 'personal': time_ranges_groups }
# time_ranges_groups: { 'time_range': (start_time, end_time), 'rankings': (urgent, deep, shallow) }[]
# urgent, deep, shallow: 1-100
# work_and_personal_tasks_transformed: { 'work': task[], 'personal': task[] }
# task: { 'id': int, 'section': int (1-4), 'priority': int (1-3), 'deadline': datetime.datetime(year, month, day, hour, min), 'time_length': int (1, 2, 4, 8), 'time_ranges': [] (later datetime.datetime(year, month, day, hour, min)[]), 'task_type': DEFAULT_TASK_TYPE (later TaskType) }
# return value specfication:
# { 'task_id_str': time_ranges[] (time_ranges sorted in sequential order) }
# can be empty if work_and_personal_tasks_transformed[workspace_type] == [] or work_and_personal_time_ranges_rankings[workspace_type] == []
def get_allocatable_tasks_time_ranges(work_and_personal_time_ranges_rankings, work_and_personal_tasks_transformed, workspace_type, parameters):
  num_tasks = len(work_and_personal_tasks_transformed[workspace_type])
  if num_tasks == 0:
    return {}
  
  num_groups = len(work_and_personal_time_ranges_rankings[workspace_type])
  i = 0
  while (i < num_groups):
    time_ranges_group = work_and_personal_time_ranges_rankings[workspace_type][i]
    task_with_max_relative_priority = {
        'task_index': 0,
        'relative_priority': 0,
        'num_time_ranges': 0,
        'task_type': DEFAULT_TASK_TYPE,
      }
    first_task_with_max_relative_priority_set = False
    
    for j in range(num_tasks):
      # priority: higher means higher priority
      # time_length: lower means higher priority
      task = work_and_personal_tasks_transformed[workspace_type][j]

      if task['time_length'] == 0:
        continue

      last_end_time = time_ranges_group[min(task['time_length'], len(time_ranges_group)) - 1]['time_range'][1]
      last_end_time_minus_hour_min = datetime(last_end_time.year, last_end_time.month, last_end_time.day)
      td_diff = task['deadline'] - last_end_time_minus_hour_min

      if td_diff.days < 0:
        continue

      # day_diff: int (0-14), lower means higher priority
      day_diff = min(td_diff.days, 14)

      # time_length_diff: int (0-7), lower means higher priority
      time_length_diff = min(abs(len(time_ranges_group) - task['time_length']), 7)

      task_type = get_task_type(task['priority'], day_diff, task['time_length'])
      task_type_index = get_task_type_index(task_type)
      
      # num_time_ranges: int (1-8), specifies how many 15 min time ranges the task will be allocated into        
      num_time_ranges = min(task['time_length'], len(time_ranges_group))
      sum_type_ranking = 0
      for k in range(num_time_ranges):
        sum_type_ranking += time_ranges_group[k]['rankings'][task_type_index]
      # average_type_ranking: int (1-100), higher means higher priority
      average_type_ranking = sum_type_ranking / num_time_ranges

      # transforms the value into range 0-1
      values_transformed = {
        'a': task['priority'] / 3,
        'b': (9 - task['time_length']) / 9,
        'c': get_day_diff_value_transformed(day_diff),
        'd': average_type_ranking / 100,
        'e': (8 - time_length_diff) / 8,
      }

      task_relative_priority = multiply_parameters_and_values(parameters, values_transformed, ['a', 'b', 'c', 'd', 'e'])

      # set the first_task_with_max_relative_priority_set 
      if not first_task_with_max_relative_priority_set:
        task_with_max_relative_priority['task_index'] = j
        task_with_max_relative_priority['relative_priority'] = task_relative_priority
        task_with_max_relative_priority['num_time_ranges'] = num_time_ranges
        task_with_max_relative_priority['task_type'] = task_type
        first_task_with_max_relative_priority_set = True
      # update task_with_max_relative_priority with the task with currently highest relative priority
      elif task_with_max_relative_priority['relative_priority'] < task_relative_priority:
          task_with_max_relative_priority['task_index'] = j
          task_with_max_relative_priority['relative_priority'] = task_relative_priority
          task_with_max_relative_priority['num_time_ranges'] = num_time_ranges
          task_with_max_relative_priority['task_type'] = task_type
    
    task_index = task_with_max_relative_priority['task_index']
    num_time_ranges = task_with_max_relative_priority['num_time_ranges']
    task_type = task_with_max_relative_priority['task_type']
    
    # if no task has been selected for task_with_relative_priority, break the loop (there are no task); this is to prevent bugs in the statements below
    if not first_task_with_max_relative_priority_set:
      break
    
    work_and_personal_tasks_transformed[workspace_type][task_index]['time_ranges'].extend([time_range['time_range'] for time_range in work_and_personal_time_ranges_rankings[workspace_type][i][:num_time_ranges]])
    work_and_personal_tasks_transformed[workspace_type][task_index]['time_length'] -= num_time_ranges
    work_and_personal_tasks_transformed[workspace_type][task_index]['task_type'] = task_type
    work_and_personal_time_ranges_rankings[workspace_type][i] = work_and_personal_time_ranges_rankings[workspace_type][i][num_time_ranges:]

    work_and_personal_tasks_transformed[workspace_type] = combine_sections_time_length(work_and_personal_tasks_transformed[workspace_type])

    tasks_with_time_length_remaining = [task for task in work_and_personal_tasks_transformed[workspace_type] if task['time_length'] != 0]
    
    # if all the tasks have been allocated, break the loop
    if len(tasks_with_time_length_remaining) == 0:
      break

    # if all the time ranges in a group has been allocated, move to the next time ranges group
    if work_and_personal_time_ranges_rankings[workspace_type][i] == []:
      i += 1

  tasks_sections_combined_and_time_ranges_sorted = combine_tasks_sections_and_time_ranges_sorted(work_and_personal_tasks_transformed[workspace_type])
  tasks_time_ranges_merged = merge_tasks_time_ranges(tasks_sections_combined_and_time_ranges_sorted)

  return tasks_time_ranges_merged

# parameter value specification:
# id: int (valid User id)
# return value specification:
# { 'work': allocatable_tasks_time_ranges, 'personal': allocatable_tasks_time_ranges }
# allocatable_tasks_time_ranges: { 'task_id_str': { 'time_ranges:' time_ranges[] (time_ranges sorted in sequential order), 'task_type': TaskType } }
# allocatable_tasks_time_ranges: can be empty if work_and_personal_tasks_transformed[workspace_type] == [] or work_and_personal_time_ranges_rankings[workspace_type] == []
def get_tasks_with_highest_relative_priority(id):
  from models import User
  user = User.query.get(id)
  (sleep_end_today_or_now, sleep_start_tomorrow) = get_one_full_day(user.sleep_time_range)

  work_and_personal_time_ranges = get_work_and_personal_time_ranges(id, sleep_end_today_or_now, sleep_start_tomorrow, user.work_time_range, user.sleep_time_range)
  
  # DEBUG
  # print('work_and_personal_time_ranges:')
  # pprint(work_and_personal_time_ranges)
  
  work_days = user.get_work_days()
  rankings = user.get_rankings()
  tasks = user.get_tasks()
  
  work_and_personal_tasks = seperate_work_and_personal_tasks(tasks)
  
  # DEBUG
  # print('work_and_personal_tasks:')
  # pprint(work_and_personal_tasks)

  work_and_personal_time_ranges_rankings = get_work_and_personal_time_ranges_rankings(
    work_and_personal_time_ranges=work_and_personal_time_ranges,
    work_days=work_days,
    rankings=rankings
  )

  # DEBUG
  # print('work_and_personal_time_ranges_rankings')
  # pprint(work_and_personal_time_ranges_rankings)

  # constant parameters for recommendation algorithm
  parameters = {
    'a': 3,
    'b': 1,
    'c': 4,
    'd': 2,
    'e': 2
  }

  work_and_personal_tasks_transformed = {
    'work': get_tasks_transformed(work_and_personal_tasks['work']), 
    'personal': get_tasks_transformed(work_and_personal_tasks['personal'])
  }

  # DEBUG
  # print('work_and_personal_tasks_transformed:')
  # pprint(work_and_personal_tasks_transformed)

  allocatable_tasks_time_ranges = {
    'work': get_allocatable_tasks_time_ranges(work_and_personal_time_ranges_rankings, work_and_personal_tasks_transformed, 'work', parameters),
    'personal': get_allocatable_tasks_time_ranges(work_and_personal_time_ranges_rankings, work_and_personal_tasks_transformed, 'personal', parameters)
  }

  return allocatable_tasks_time_ranges