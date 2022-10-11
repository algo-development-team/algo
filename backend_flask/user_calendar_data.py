from models import User
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from dotenv import load_dotenv
load_dotenv()
import os
from datetime import datetime, timedelta
from pprint import pprint

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
TOKEN_URI = 'https://oauth2.googleapis.com/token'

# parameter specification:
# time_range_simple_str: 'H:MM' or 'HH:MM'
def parse_user_time_range(user_time_range):
  [hour, min] = user_time_range.split(':')
  return { 'hour': hour, 'min': min }

def get_user_time_zone(id):
  user = User.query.get(id)
  creds = Credentials(token=None, refresh_token=user.refresh_token, token_uri=TOKEN_URI, client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
  service = build('calendar', 'v3', credentials=creds)
  time_zone = service.settings().get(setting='timezone').execute()
  return time_zone['value']

def get_user_calendar_id_list(id):
  user = User.query.get(id)
  creds = Credentials(token=None, refresh_token=user.refresh_token, token_uri=TOKEN_URI, client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
  service = build('calendar', 'v3', credentials=creds)

  response = service.calendarList().list(
    maxResults=250,
    showDeleted=False,
    showHidden=False,
  ).execute()

  calendarItems = response.get('items')
  nextPageToken = response.get('nextPageToken')

  while nextPageToken:
    response = service.calendarList().list(
      maxResults=250,
      showDeleted=False,
      showHidden=False,
      pageToken=nextPageToken,
    ).execute()
    calendarItems.extend(response.get('items'))
    nextPageToken = response.get('nextPageToken')

  # DEBUG
  # pprint([(calendar['summary'], calendar['id']) for calendar in calendarItems])

  calendar_id_list = [calendar['id'] for calendar in calendarItems]
 
  return calendar_id_list

# STOPPED HERE
# debug the code below

# helper function
# returns a new list of new_events inserted into events in sequential order
# pure function: does not modify the given parameters
def seq_insert_new_events_into_events(events, new_events):
  events_copy = events[:]
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
def get_user_events_time_range(id, time_min, time_max, only_primary=False):
  user = User.query.get(id)
  creds = Credentials(token=None, refresh_token=user.refresh_token, token_uri=TOKEN_URI, client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
  service = build('calendar', 'v3', credentials=creds)
  # adding buffer time to time_min (previous day - 2h 15 min) and time_max (next day + 2h 15 min)
  time_min_with_buffer = datetime(time_min.year, time_min.month, time_min.day) - timedelta(days=1, hours=2, minutes=15)
  time_max_with_buffer = datetime(time_min.year, time_min.month, time_min.day) + timedelta(days=2, hours=2, minutes=15)
  time_min_str = time_min_with_buffer.strftime('%Y-%m-%dT%H:%M:00Z')
  time_max_str = time_max_with_buffer.strftime('%Y-%m-%dT%H:%M:00Z')
  calendar_id_list = get_user_calendar_id_list(id)
  
  events = []
  result = []
  if only_primary:
    events_result = service.events().list(calendarId='primary', timeMin=time_min_str, timeMax=time_max_str, singleEvents=True, orderBy='startTime').execute()
    events += events_result['items']
  else:
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

# parameter specification:
# time_ranges: [(start_time, end_time), (start_time, end_time), ...]
# start_time: datetime.datetime(year, month, day, hour, min)
# end_time: datetime.datetime(year, month, day, hour, min)
# return value specification:
# [(start_time, end_time), (start_time, end_time), ...]
def get_dt_fifteen_min_rounded(time_ranges):
  # round down in fifteen
  def start_time_round(dt): 
    start_time_round_timedelta = timedelta(minutes=(dt.minute % 15))
    return dt - start_time_round_timedelta
  # round up in fifteen
  def end_time_round(dt): 
    end_time_round_timedelta_val = 15 - (dt.minute % 15)
    if end_time_round_timedelta_val == 15:
      end_time_round_timedelta_val = 0
    end_time_round_timedelta = timedelta(minutes=end_time_round_timedelta_val)
    return dt + end_time_round_timedelta
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
# [(start_time, end_time, duration), (start_time, end_time, duration), ...]
def get_empty_time_ranges_and_durations(id, time_min, time_max):
  time_ranges = get_dt_fifteen_min_rounded(get_user_events_time_range(id, time_min, time_max))
  time_ranges_detupled = [time_min]
  for time_range in time_ranges:
    time_ranges_detupled.append(time_range[0])
    time_ranges_detupled.append(time_range[1])
  time_ranges_detupled.append(time_max)

  empty_time_ranges_durations = []
  for i in range(0, len(time_ranges_detupled), 2):
    diff = int((time_ranges_detupled[i+1] - time_ranges_detupled[i]).total_seconds() / 60)
    if diff > 0:
      empty_time_ranges_durations.append((time_ranges_detupled[i], time_ranges_detupled[i+1], diff))

  return empty_time_ranges_durations

################################################################

# TEST

# use dts for testing get_dt_fifteen_min_rounded
dt1 = datetime(2022, 10, 9, 0, 18)
dt2 = datetime(2022, 10, 9, 0, 42)
dt3 = datetime(2022, 10, 9, 0, 27)
dt4 = datetime(2022, 10, 9, 0, 33)
dts = [(dt1, dt2), (dt3, dt4)]

# test string time comparison
str_ts = ['2022-10-10T08:45:00-04:00',
          '2022-10-10T16:30:00-04:00',
          '2022-10-11T13:00:00-04:00',
          '2022-10-11T14:30:00-04:00',
          '2022-10-12T10:30:00-04:00',
          '2022-10-12T14:30:00-04:00',
          '2022-10-12T16:30:00-04:00',
          '2022-10-11T12:00:00-04:00']

################################################################