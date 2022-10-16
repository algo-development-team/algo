from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import user
import auth
import workspace
import category
import task
import schedule
from dotenv import load_dotenv
load_dotenv()
import os

app = Flask(__name__)
api = Api(app)
CORS(app)

DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_DEVELOPMENT_STAGE = os.getenv('DB_DEVELOPMENT_STAGE')
DB_PROJECT_NAME = os.getenv('DB_PROJECT_NAME')

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:{DB_PASSWORD}@{DB_DEVELOPMENT_STAGE}/{DB_PROJECT_NAME}'
db = SQLAlchemy(app)

migrate = Migrate(app, db)

app.register_blueprint(auth.bp)
app.register_blueprint(user.bp)
app.register_blueprint(workspace.bp)
app.register_blueprint(category.bp)
app.register_blueprint(task.bp)
app.register_blueprint(schedule.bp)

@app.route('/')
def hello_world():
  return f'Algo Backend app Route'

if __name__ == '__main__':
  app.run(debug=True)