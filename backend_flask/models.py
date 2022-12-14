from app import db
from sqlalchemy import ARRAY, Enum
import enum

default_work_time_range = '9:00-17:00'
default_sleep_time_range = '23:00-7:00'
default_work_days = [False, True, True, True, True, True, False]
default_rankings = [50] * 24

class WorkspaceType(enum.Enum):
  WORK = 1
  PERSONAL = 2

class Priority(enum.Enum):
  LOW = 1
  AVERAGE = 2
  HIGH = 3

class TimeLength(enum.Enum):
  FIFTEEN_MIN = 1
  THIRTY_MIN = 2
  ONE_HOUR = 3
  TWO_HOURS = 4
  FOUR_HOURS = 5
  EIGHT_HOURS = 6

# enum numeric value equivalent to the work_type_index
class TaskType(enum.Enum):
  NONE = -1
  URGENT = 0
  DEEP = 1
  SHALLOW = 2

def get_workspace_type(workspace_type):
  if workspace_type == 'WORK':
    return WorkspaceType.WORK
  elif workspace_type == 'PERSONAL':
    return WorkspaceType.PERSONAL

def get_priority(priority):
  if priority == 'LOW':
    return Priority.LOW
  elif priority == 'AVERAGE':
    return Priority.AVERAGE
  elif priority == 'HIGH':
    return Priority.HIGH

def get_time_length(time_length):
  if time_length == 'FIFTEEN_MIN':
    return TimeLength.FIFTEEN_MIN
  elif time_length == 'THIRTY_MIN':
    return TimeLength.THIRTY_MIN
  elif time_length == 'ONE_HOUR':
    return TimeLength.ONE_HOUR
  elif time_length == 'TWO_HOURS':
    return TimeLength.TWO_HOURS
  elif time_length == 'FOUR_HOURS':
    return TimeLength.FOUR_HOURS
  elif time_length == 'EIGHT_HOURS':
    return TimeLength.EIGHT_HOURS

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(160), nullable=False)
  email = db.Column(db.String(320), unique=True, nullable=False)
  picture = db.Column(db.String(160), nullable=False)
  refresh_token = db.Column(db.String(160), unique=True, nullable=False)
  work_time_range = db.Column(db.String(80), nullable=False, default=default_work_time_range)
  sleep_time_range = db.Column(db.String(80), nullable=False, default=default_sleep_time_range)
  work_days = db.Column(ARRAY(db.Boolean), nullable=False, default=default_work_days)
  is_setup = db.Column(db.Boolean, nullable=False, default=False)
  calendar_id = db.Column(db.String(160), unique=True, nullable=False)

  checklist = db.Column(ARRAY(db.Integer), nullable=False, default=[])
  
  urgent_rankings_ww = db.Column(ARRAY(db.Integer), nullable=False, default=default_rankings)
  deep_rankings_ww = db.Column(ARRAY(db.Integer), nullable=False, default=default_rankings)
  shallow_rankings_ww = db.Column(ARRAY(db.Integer), nullable=False, default=default_rankings)
  urgent_rankings_pw = db.Column(ARRAY(db.Integer), nullable=False, default=default_rankings)
  deep_rankings_pw = db.Column(ARRAY(db.Integer), nullable=False, default=default_rankings)
  shallow_rankings_pw = db.Column(ARRAY(db.Integer), nullable=False, default=default_rankings)
  urgent_rankings_pnw = db.Column(ARRAY(db.Integer), nullable=False, default=default_rankings)
  deep_rankings_pnw = db.Column(ARRAY(db.Integer), nullable=False, default=default_rankings)
  shallow_rankings_pnw = db.Column(ARRAY(db.Integer), nullable=False, default=default_rankings)
  tasks = db.relationship('Task', backref='user', lazy=True, cascade='delete, merge, save-update')

  def __repr__(self):
    return f'User({self.name}, {self.email}, {self.work_time_range}, {self.sleep_time_range})'    

  def serialize(self):
    return {
      'id': self.id,
      'name': self.name,
      'email': self.email,
      'picture': self.picture,
      'refresh_token': self.refresh_token,
      'work_time_range': self.work_time_range,
      'sleep_time_range': self.sleep_time_range,
      'work_days': self.work_days,
      'is_setup': self.is_setup,
      'calendar_id': self.calendar_id,
      'checklist': self.checklist,
      'urgent_rankings_ww': self.urgent_rankings_ww,
      'deep_rankings_ww': self.deep_rankings_ww,
      'shallow_rankings_ww': self.shallow_rankings_ww,
      'urgent_rankings_pw': self.urgent_rankings_pw,
      'deep_rankings_pw': self.deep_rankings_pw,
      'shallow_rankings_pw': self.shallow_rankings_pw,
      'urgent_rankings_pnw': self.urgent_rankings_pnw,
      'deep_rankings_pnw': self.deep_rankings_pnw,
      'shallow_rankings_pnw': self.shallow_rankings_pnw,
      'tasks': [task.serialize() for task in self.tasks]
    }

  def get_work_days(self):
    return self.work_days[:]

  def get_checklist(self):
    return self.checklist[:]

  def get_tasks(self):
    return self.tasks[:]

  def get_rankings(self):
    return {
      'urgent_rankings_ww': self.urgent_rankings_ww[:],
      'deep_rankings_ww': self.deep_rankings_ww[:],
      'shallow_rankings_ww': self.shallow_rankings_ww[:],
      'urgent_rankings_pw': self.urgent_rankings_pw[:],
      'deep_rankings_pw': self.deep_rankings_pw[:],
      'shallow_rankings_pw': self.shallow_rankings_pw[:],
      'urgent_rankings_pnw': self.urgent_rankings_pnw[:],
      'deep_rankings_pnw': self.deep_rankings_pnw[:],
      'shallow_rankings_pnw': self.shallow_rankings_pnw[:]
    }

class Workspace(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(10000), nullable=False)
  workspace_type = db.Column(Enum(WorkspaceType), nullable=False)
  members = db.Column(ARRAY(db.Integer), nullable=False)
  admins = db.Column(ARRAY(db.Integer), nullable=False)
  categories = db.relationship('Category', backref='workspace', lazy=True, cascade='delete, merge, save-update')

  def __repr__(self):
    return f'Workspace({self.name}, {self.workspace_type})'

  def serialize(self):
    return {
      'id': self.id,
      'name': self.name,
      'workspace_type': self.workspace_type.name,
      'members': self.members,
      'admins': self.admins,
      'categories': [category.serialize() for category in self.categories]
    }

  def get_members(self):
    return self.members[:]

  def get_admins(self):
    return self.admins[:]

  def get_categories(self):
    return self.categories[:]

class Category(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80), nullable=False)
  workspace_id = db.Column(db.Integer, db.ForeignKey('workspace.id'), nullable=False)
  tasks = db.relationship('Task', backref='category', lazy=True, cascade='delete, merge, save-update')

  def __repr__(self):
    return f'Category({self.name})'

  def serialize(self):
    return {
      'id': self.id,
      'name': self.name,
      'tasks': [task.serialize() for task in self.tasks]
    }

  def get_tasks(self):
    return self.tasks[:]

class Task(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(10000), nullable=False)
  description = db.Column(db.String(10000), nullable=False)
  priority = db.Column(Enum(Priority), nullable=False)
  deadline = db.Column(db.DateTime, nullable=False)
  time_length = db.Column(Enum(TimeLength), nullable=False)
  completed = db.Column(db.Boolean, nullable=False, default=False)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

  def __repr__(self):
    return f'Task({self.title}, {self.description}, {self.priority}, {self.deadline}, {self.time_length}, {self.completed})'

  def serialize(self):
    return {
      'id': self.id,
      'title': self.title,
      'description': self.description,
      'priority': self.priority.name,
      'deadline': self.deadline,
      'time_length': self.time_length.name,
      'completed': self.completed
    }