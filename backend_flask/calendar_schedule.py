from recommendation_algorithm import get_tasks_with_highest_relative_priority
from user_calendar_data import get_user_events_time_range
from models import Task, User, TaskType
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import os
from datetime import datetime, timedelta
from pprint import pprint

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
TOKEN_URI = 'https://oauth2.googleapis.com/token'

# Color ID:
# 1 blue
# 2 green
# 3 purple
# 4 red
# 5 yellow
# 6 orange
# 7 turquoise
# 8 grey
# 9 bold blue
# 10 bold green
# 11 bold red

# helper function
# parameters specification:
# task_type: TaskType
def get_color_id(task_type):
  if task_type == TaskType.NONE:
    return 8
  elif task_type == TaskType.URGENT:
    return 6
  elif task_type == TaskType.DEEP:
    return 7
  elif task_type == TaskType.SHALLOW:
    return 2

# helper function
# parameters specification:
# tasks: { 'task_id_str': { 'task_type': TaskType, 'time_ranges': (start_time, end_time)[] },... }
# start_time: datetime.datetime(year, month, day, hour, min)
# end_time: datetime.datetime(year, month, day, hour, min)
def get_events(tasks, time_zone):
  events = []
  for task_id_str in tasks:
    task = tasks[task_id_str]
    task_obj = Task.query.get(int(task_id_str))
    color_id = get_color_id(task['task_type'])
    for time_range in task['time_ranges']:
      start_time = time_range[0]
      end_time = time_range[1]
      event = {
        'summary': task_obj.title,
        'description': task_obj.description,
        'start': {
          'dateTime': start_time.strftime('%Y-%m-%dT%H:%M:%S'),
          'timeZone': time_zone,
        },
        'end': {
          'dateTime': end_time.strftime('%Y-%m-%dT%H:%M:%S'),
          'timeZone': time_zone,
        },
        'colorId': color_id,
      }
      events.append(event)
  return events

# helper function
def get_first_time_and_last_time(allocatable_tasks_time_ranges):
  time_ranges = sum([sum([task_values['time_ranges'] for task_values in list(allocatable_tasks_time_ranges['work'].values())], []),
                     sum([task_values['time_ranges'] for task_values in list(allocatable_tasks_time_ranges['personal'].values())], [])], [])
  time_ranges.sort(key=lambda time_range: time_range[0])                  

  first_time = time_ranges[0][0]
  last_time = time_ranges[len(time_ranges) - 1][1]

  return (first_time, last_time)

# helper function
def get_allocated_events(id, first_time, last_time):
  allocated_events = get_user_events_time_range(id, first_time, last_time, algo=True, include_event_ids=True, mark_edge_events=True)
  return allocated_events

def add_task_time_blocks_to_calendar(id, calendar_id, refresh_token, time_zone):
  allocatable_tasks_time_ranges = get_tasks_with_highest_relative_priority(id)

  # DEBUG
  # print('allocatable_tasks_time_ranges:')
  # pprint(allocatable_tasks_time_ranges)

  (first_time, last_time) = get_first_time_and_last_time(allocatable_tasks_time_ranges)

  # allocated_events data structure
  # [(start_time, end_time, event_id, is_edge_event),...]
  # is_edge_event: int (0-2) (0 for false, 1 for start edge event, 2 for end edge event)
  allocated_events = get_allocated_events(id, first_time, last_time)

  # DEBUG
  # print('allocated_events')
  # pprint(allocated_events)

  events = []
  events.extend(get_events(allocatable_tasks_time_ranges['work'], time_zone))
  events.extend(get_events(allocatable_tasks_time_ranges['personal'], time_zone))

  # DEBUG
  # print('events:')
  # pprint(events)

  creds = Credentials(token=None, refresh_token=refresh_token, token_uri=TOKEN_URI, client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
  service = build('calendar', 'v3', credentials=creds)

  for allocated_event in allocated_events:
    if allocated_event[3] == 1:
      original_event = service.events().get(calendarId=calendar_id, eventId=allocated_event[2]).execute()
      original_event['end']['dateTime'] = first_time.strftime('%Y-%m-%dT%H:%M:%S')
      updated_event = service.events().update(calendarId=calendar_id, eventId=original_event['id'], body=original_event).execute()
      # DEBUG
      # print('updated_event:')
      # pprint(updated_event)         
    elif allocated_event[3] == 2:
      original_event = service.events().get(calendarId=calendar_id, eventId=allocated_event[2]).execute()
      original_event['start']['dateTime'] = last_time.strftime('%Y-%m-%dT%H:%M:%S')
      updated_event = service.events().update(calendarId=calendar_id, eventId=original_event['id'], body=original_event).execute()
      # DEBUG
      # print('updated_event:')
      # pprint(updated_event)         
    else:
      service.events().delete(calendarId=calendar_id, eventId=allocated_event[2]).execute()
      # DEBUG
      # print('deleted event: ' + allocated_event[2])

  for event in events:
    created_event = service.events().insert(calendarId=calendar_id, body=event).execute()
    # DEBUG
    # print('created_event:')
    # pprint(created_event)         

# TEST 
def test():
  user = User.query.get(4)
  add_task_time_blocks_to_calendar(user.id, user.calendar_id, user.refresh_token, 'America/Winnipeg')

test()