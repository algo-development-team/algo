# FUTURE CHANGES
# get_user_events_time_range should have an additional field that takes in which calendars' tasks are fetched

from models import User
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from dotenv import load_dotenv
load_dotenv()
import os
from datetime import datetime, timedelta
from copy import deepcopy
from pprint import pprint

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
TOKEN_URI = 'https://oauth2.googleapis.com/token'

# parameter specification:
# user_time_range: 'Hour:MM-Hour:MM', where Hour is 'H' or 'HH'
# return value specification:
# { 'start': { 'hour': int, 'minute': int }, 'end': { 'hour': int, 'minute': int } }
def parse_user_time_range(user_time_range):
  time_limit_hour_and_minute_str = [[int(time_limit_part) for time_limit_part in time_limit.split(':')] for time_limit in user_time_range.split('-')]
  return { 
    'start': { 
      'hour': time_limit_hour_and_minute_str[0][0], 
      'minute': time_limit_hour_and_minute_str[0][1]
    }, 
    'end': {
      'hour': time_limit_hour_and_minute_str[1][0],
      'minute': time_limit_hour_and_minute_str[1][1]
    } 
  }

def get_user_time_zone(id):
  user = User.query.get(id)
  creds = Credentials(token=None, refresh_token=user.refresh_token, token_uri=TOKEN_URI, client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
  service = build('calendar', 'v3', credentials=creds)
  time_zone = service.settings().get(setting='timezone').execute()
  return time_zone['value']

# helper function
def get_user_calendar_id_list(id):
  user = User.query.get(id)
  creds = Credentials(token=None, refresh_token=user.refresh_token, token_uri=TOKEN_URI, client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
  service = build('calendar', 'v3', credentials=creds)

  calendar_list = service.calendarList().list(
    maxResults=50,
    showDeleted=False,
    showHidden=False,
  ).execute()

  calendar_id_list = [calendar['id'] for calendar in calendar_list['items']]
 
  return calendar_id_list

# helper function
# returns a new list of new_events inserted into events in sequential order
def seq_insert_new_events_into_events(events, new_events):
  events_copy = [deepcopy(event) for event in events]
  for new_event in new_events:
    for i in range(len(events_copy)):
      if new_event['start']['dateTime'] < events_copy[i]['start']['dateTime']:
        events_copy.insert(i, new_event)
        break
  return events_copy

# parameters specification:
# id: user_id that has valid refresh_token (non-test user)
# time_min: datetime.datetime(year, month, day, hour, min)
# time_max: datetime.datetime(year, month, day, hour, min)
# time_min_str (inside the function, not a parameter): 'YYYY-MM-DDTHH:MM:SSZ'
# time_max_str (inside the function, not a parameter): 'YYYY-MM-DDTHH:MM:SSZ'
# time_min < time_max
# return value specification:
# [(start_time, end_time), (start_time, end_time), ...]
# start_time_str (inside the function): 'YYYY-MM-DDTHH:MM:SS-HH:MM'
# end_time_str (inside the function): 'YYYY-MM-DDTHH:MM:SSZ-HH:MM'
# start_time: datetime.datetime(year, month, day, hour, min)
# end_time: datetime.datetime(year, month, day, hour, min)
def get_user_events_time_range(id, time_min, time_max):
  user = User.query.get(id)
  creds = Credentials(token=None, refresh_token=user.refresh_token, token_uri=TOKEN_URI, client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
  service = build('calendar', 'v3', credentials=creds)
  # adding buffer time to time_min (previous day - 2h 15 min) and time_max (next day + 2h 15 min)
  time_min_with_buffer = datetime(time_min.year, time_min.month, time_min.day) - timedelta(days=1, hours=2, minutes=15)
  time_max_with_buffer = datetime(time_min.year, time_min.month, time_min.day) + timedelta(days=2, hours=2, minutes=15)
  time_min_str = time_min_with_buffer.strftime('%Y-%m-%dT%H:%M:00Z')
  time_max_str = time_max_with_buffer.strftime('%Y-%m-%dT%H:%M:00Z')
  events = []
  result = []
  calendar_id_list = get_user_calendar_id_list(id)
  for calendar_id in calendar_id_list:
    events_result = service.events().list(calendarId=calendar_id, timeMin=time_min_str, timeMax=time_max_str, singleEvents=True, orderBy='startTime').execute()
    new_events = events_result['items']
    # only keep events that have both start and end time
    new_events_with_time_range = [event for event in new_events if 'dateTime' in event['start'] and 'dateTime' in event['end']]
    if len(events) == 0:
      events = new_events_with_time_range
    else:  
      result = seq_insert_new_events_into_events(events, new_events_with_time_range)
      events = result

  remove_dt_tzinfo = lambda dt_tzinfo : datetime(dt_tzinfo.year, dt_tzinfo.month, dt_tzinfo.day, dt_tzinfo.hour, dt_tzinfo.minute) 
  events_time_range = [(
    remove_dt_tzinfo(datetime.strptime(event['start']['dateTime'], '%Y-%m-%dT%H:%M:%S%z')), 
    remove_dt_tzinfo(datetime.strptime(event['end']['dateTime'], '%Y-%m-%dT%H:%M:%S%z'))) 
    for event in events]
  # eliminate time ranges that are in the buffer time, where the cut off for events at the edge are at time_min and time_max
  events_time_range_remove_buffer = []
  for event_time_range in events_time_range:
    if event_time_range[0] >= time_min and event_time_range[1] <= time_max:
      events_time_range_remove_buffer.append(event_time_range)
    elif event_time_range[0] <= time_min < event_time_range[1]:
      events_time_range_remove_buffer.append((time_min, event_time_range[1]))
    elif event_time_range[0] < time_max <= event_time_range[1]:
      events_time_range_remove_buffer.append((event_time_range[0], time_max))

  return events_time_range_remove_buffer

# round down in fifteen minutes for datetime.datetime object
def start_time_round(dt): 
  start_time_round_timedelta = timedelta(minutes=(dt.minute % 15))
  return dt - start_time_round_timedelta

# round up in fifteen minutes for datetime.datetime object
def end_time_round(dt): 
  end_time_round_timedelta_val = 15 - (dt.minute % 15)
  if end_time_round_timedelta_val == 15:
    end_time_round_timedelta_val = 0
  end_time_round_timedelta = timedelta(minutes=end_time_round_timedelta_val)
  return dt + end_time_round_timedelta

# parameter specification:
# time_ranges: [(start_time, end_time), (start_time, end_time), ...]
# start_time: datetime.datetime(year, month, day, hour, min)
# end_time: datetime.datetime(year, month, day, hour, min)
# return value specification:
# [(start_time, end_time), (start_time, end_time), ...]
# start_time: datetime.datetime(year, month, day, hour, min)
# end_time: datetime.datetime(year, month, day, hour, min)
def get_dt_fifteen_min_rounded(time_ranges):
  time_ranges_rounded = [
    (start_time_round(time_range[0]), 
    end_time_round(time_range[1]))
    for time_range in time_ranges]
  return time_ranges_rounded

# parameters specification:
# id: user_id that has valid refresh_token (non-test user)
# time_min: datetime.datetime(year, month, day, hour, min)
# time_max: datetime.datetime(year, month, day, hour, min)
# return value specification:
# [(start_time, end_time), (start_time, end_time), ...]
# start_time: datetime.datetime(year, month, day, hour, min), min rounded to 15 min
# end_time: datetime.datetime(year, month, day, hour, min), min rounded to 15 min
def get_empty_time_ranges(id, time_min, time_max):
  time_ranges = get_dt_fifteen_min_rounded(get_user_events_time_range(id, time_min, time_max))
  time_ranges_detupled = [time_min]
  for time_range in time_ranges:
    time_ranges_detupled.append(time_range[0])
    time_ranges_detupled.append(time_range[1])
  time_ranges_detupled.append(time_max)

  empty_time_ranges = []
  for i in range(0, len(time_ranges_detupled), 2):
    diff = int((time_ranges_detupled[i+1] - time_ranges_detupled[i]).total_seconds() / 60)
    if diff > 0:
      empty_time_ranges.append((time_ranges_detupled[i], time_ranges_detupled[i+1]))

  return empty_time_ranges

# helper function
def get_period_limit_type(period_limits_idx):
  if period_limits_idx == 0:
    return 'sleep_end'
  elif period_limits_idx == 1:
    return 'work_start'
  elif period_limits_idx == 2:
    return 'work_end'
  elif period_limits_idx == 3:
    return 'sleep_start'

# helper function
# parameter specification:
# time_range: (start_time, end_time)
# start_time: datetime.datetime(year, month, day, hour, min)
# end_time: datetime.datetime(year, month, day, hour, min)
# work_time_range: { 'start': { 'hour': int, 'min': int }, 'end': { 'hour': int, 'min': int } }
# sleep_time_range: { 'start': { 'hour': int, 'min': int }, 'end': { 'hour': int, 'min': int } }
# return value specification:
# [{ 'type': str, 'time': datetime.datetime(year, month, day, hour, min) }, ...]
def get_period_ranges(time_range, work_time_range, sleep_time_range):
  convert_minute_only = lambda hour, minute : hour * 60 + minute
  (start_time, end_time) = time_range
  start_time_minute = convert_minute_only(start_time.hour, start_time.minute)
  sleep_end_minute = convert_minute_only(sleep_time_range['end']['hour'], sleep_time_range['end']['minute'])
  sleep_end1 = datetime(start_time.year, start_time.month, start_time.day, sleep_time_range['end']['hour'], sleep_time_range['end']['minute'])
  if start_time_minute < sleep_end_minute:
    sleep_end1 -= timedelta(days=1)
  round = 1
  range_limits = [{ 'type': 'sleep_end', 'time': sleep_end1 }]
  period_limits = [sleep_time_range['end'], work_time_range['start'], work_time_range['end'], sleep_time_range['start']]
  period_limits_idx = 1
  time_reference = datetime(sleep_end1.year, sleep_end1.month, sleep_end1.day)
  while (round <= 4):
    if period_limits_idx == 4:
      period_limits_idx = 0
      round += 1
    current_range_limit_minute = convert_minute_only(period_limits[period_limits_idx]['hour'], period_limits[period_limits_idx]['minute'])
    previous_range_limit = range_limits[len(range_limits) - 1]
    previous_range_limit_minute = convert_minute_only(previous_range_limit['time'].hour, previous_range_limit['time'].minute)
    if current_range_limit_minute < previous_range_limit_minute:
      time_reference += timedelta(days=1)
    new_range_limit = datetime(time_reference.year, time_reference.month, time_reference.day, period_limits[period_limits_idx]['hour'], period_limits[period_limits_idx]['minute'])  
    range_limits.append({ 'type': get_period_limit_type(period_limits_idx), 'time': new_range_limit })
    # last range limit
    if end_time <= new_range_limit:
      break
    # another range limit  
    period_limits_idx += 1
  
  return range_limits

def get_period_type(type_before, type_after, start_time, work_days):
  if type_before == 'sleep_end' and type_after == 'work_start':
    return { 'type': 'personal'  }
  elif type_before == 'work_start' and type_after == 'work_end':
    is_work_day = work_days[int(start_time.date().strftime('%w'))]
    if is_work_day:
      return { 'type': 'work' }
    else:
      return { 'type': 'personal' }
  elif type_before == 'work_end' and type_after == 'sleep_start':
    return { 'type': 'personal' }
  elif type_before == 'sleep_start' and type_after == 'sleep_end':
    return { 'type': 'sleep' }

# parameter specification:
# time_ranges: [(start_time, end_time), (start_time, end_time), ...]
# start_time: datetime.datetime(year, month, day, hour, min)
# end_time: datetime.datetime(year, month, day, hour, min)
# work_time_range: 'Hour:MM-Hour:MM', where Hour is 'H' or 'HH'
# sleep_time_range: 'Hour:MM-Hour:MM', where Hour is 'H' or 'HH'
# return value specification:
# { 'work': (start_time, end_time)[], 'personal': (start_time, end_time)[] }
# start_time: datetime.datetime(year, month, day, hour, min)
# end_time: datetime.datetime(year, month, day, hour, min)
def separate_periods_time_ranges(id, time_ranges, work_time_range, sleep_time_range):
  from models import User

  user = User.query.get(id)
  work_days = user.get_work_days()

  parsed_work_time_range = parse_user_time_range(work_time_range)
  parsed_sleep_time_range = parse_user_time_range(sleep_time_range)
  work_and_personal_time_ranges = {'work': [], 'personal': []}
  for time_range in time_ranges:
    period_ranges = get_period_ranges(time_range, parsed_work_time_range, parsed_sleep_time_range)
    # DEBUG
    # print('time_range:')
    # pprint(time_range)
    # print('period_ranges:')
    # pprint(period_ranges)
    start_time = time_range[0]
    end_time = time_range[1]
    for i in range(len(period_ranges) - 1):
      if period_ranges[i]['time'] <= start_time < period_ranges[i + 1]['time']:
        # DEBUG
        # print('event starts in period ' + str(i))
        period_type = get_period_type(period_ranges[i]['type'], period_ranges[i + 1]['type'], period_ranges[i]['time'], work_days)
        # DEBUG
        # print('period_type: ' + period_type['type'])
        if period_type['type'] != 'sleep':
          if end_time <= period_ranges[i + 1]['time']:
            work_and_personal_time_ranges[period_type['type']].append((start_time, end_time))
            # DEBUG
            # pprint((start_time, end_time, 'break'))
            break
          else:
            work_and_personal_time_ranges[period_type['type']].append((start_time, period_ranges[i + 1]['time']))
            # DEBUG
            # pprint((start_time, period_ranges[i + 1]['time'], 'not break'))
        # DEBUG
        # print('start_time reset')
        start_time = period_ranges[i + 1]['time']
    
  return work_and_personal_time_ranges

# wrapper function for get_empty_time_ranges and separate_periods_time_ranges
# parameter specification:
# id: user_id that has valid refresh_token (non-test user)
# time_min: datetime.datetime(year, month, day, hour, min)
# time_max: datetime.datetime(year, month, day, hour, min)
# work_time_range: 'Hour:MM-Hour:MM', where Hour is 'H' or 'HH'
# sleep_time_range: 'Hour:MM-Hour:MM', where Hour is 'H' or 'HH'
# return value specification:
# { 'work': (start_time, end_time)[], 'personal': (start_time, end_time)[] }
# start_time: datetime.datetime(year, month, day, hour, min), min rounded to 15 min
# end_time: datetime.datetime(year, month, day, hour, min), min rounded to 15 min
def get_work_and_personal_time_ranges(id, time_min, time_max, work_time_range, sleep_time_range):
  empty_time_ranges = get_empty_time_ranges(id, time_min, time_max)
  work_and_personal_time_ranges = separate_periods_time_ranges(id, empty_time_ranges, work_time_range, sleep_time_range)
  return work_and_personal_time_ranges