from flask import Blueprint, request
from google_api import get_flow 
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from dotenv import load_dotenv
load_dotenv()
import os

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REFRESH_TOKEN = os.getenv('REFRESH_TOKEN') # FOR TESTING ONLY
TOKEN_URI = 'https://oauth2.googleapis.com/token'
USER_TIMEZONE = 'America/Toronto' # FOR TESTING ONLY
flow = None

bp = Blueprint('/api/auth', __name__, url_prefix='/api/auth')

@bp.route('/create-tokens', methods=['PUT'])
def create_tokens_handler():
  from app import db
  from models import User

  data = request.get_json()
  code = data['code']
  print(code)
  
  global flow
  flow = get_flow()
  flow.fetch_token(code=code)
  credentials = flow.credentials
  print(credentials.refresh_token)

  # regular auth, user info is not altered
  if credentials.refresh_token is None:

    return 'Auth Completed'

  # new auth, user info is created or updated
  else:
    # get Google account information about the user
    # google session information format
    # {'id': str, 'email': str, 'verified_email': bool, 'name': str, 'given_name': str, 'family_name': str, 'picture': str (url), 'locale': str}
    session = flow.authorized_session()
    user_info = session.get('https://www.googleapis.com/userinfo/v2/me').json()
    
    # DEBUG
    print(user_info)
  
    user = User.query.filter_by(email=user_info['email']).first()
    if user is None:
      creds = Credentials(token=None, refresh_token=credentials.refresh_token, token_uri=TOKEN_URI, client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
      service = build('calendar', 'v3', credentials=creds)
      time_zone = service.settings().get(setting='timezone').execute()
      calendar = {
          'summary': 'Algo',
          'timeZone': time_zone['value']
      }
      created_calendar = service.calendars().insert(body=calendar).execute()

      # DEBUG
      print(created_calendar['id'])

      user = User(name=user_info['name'], email=user_info['email'], picture=user_info['picture'], refresh_token=credentials.refresh_token, calendar_id=created_calendar['id'])
      db.session.add(user)
      db.session.commit()
      
      # DEBUG
      print('User Created')
    else:
      user.refresh_token = credentials.refresh_token
      db.session.commit()
      
      # DEBUG
      print('User Refresh Token Updated')

  return 'Token Created'

@bp.route('/create-event', methods=['POST'])
def create_event_handler():
  data = request.get_json()

  event = {
    'summary': data['summary'],
    'location': data['location'],
    'description': data['description'],
    'start': {
      'dateTime': data['startDateTime'] + ':00',
      'timeZone': USER_TIMEZONE,
    },
    'end': {
      'dateTime': data['endDateTime'] + ':00',
      'timeZone': USER_TIMEZONE,
    },
  }

  creds = Credentials(token=None, refresh_token=REFRESH_TOKEN, token_uri=TOKEN_URI, client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
  service = build('calendar', 'v3', credentials=creds)
  event = service.events().insert(calendarId='primary', body=event).execute()
  
  # DEBUG
  print(event.get('htmlLink'))

  return 'Create Event'