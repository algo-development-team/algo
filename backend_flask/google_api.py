import google_auth_oauthlib.flow
from dotenv import load_dotenv
load_dotenv()
import os

def get_flow():
  flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
      'client_secret.json',
      scopes=['https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/userinfo.email', 'openid'])

  flow.redirect_uri = os.getenv('FRONTEND_URL')
  return flow