from app import db
from models import User, Workspace, Category, Task, Priority, TimeLength, WorkspaceType
from datetime import datetime, timedelta

print('Enter the user\'s email address:')
email = input()

# remove all existing tasks, categories, and workspaces
Task.query.delete()
db.session.commit()

Category.query.delete()
db.session.commit()

Workspace.query.delete()
db.session.commit()

user = User.query.filter_by(email=email).first()

workspace_name1 = 'Workspace 1'
workspace_workspace_type1 = WorkspaceType.WORK
workspace_members1 = [user.id]
workspace_admins1 = [user.id]
workspace1 = Workspace(name=workspace_name1, workspace_type=workspace_workspace_type1, members=workspace_members1, admins=workspace_admins1)
workspace_name2 = 'Workspace 2'
workspace_workspace_type2 = WorkspaceType.PERSONAL
workspace_members2 = [user.id]
workspace_admins2 = [user.id]
workspace2 = Workspace(name=workspace_name2, workspace_type=workspace_workspace_type2, members=workspace_members2, admins=workspace_admins2)

# input user specific workspaces
db.session.add(workspace1)
db.session.add(workspace2)
db.session.commit()

category_name1 = 'Category 1'
category1 = Category(name=category_name1, workspace_id=workspace1.id)
category_name2 = 'Category 2'
category2 = Category(name=category_name2, workspace_id=workspace2.id)

# input user specific categories
db.session.add(category1)
db.session.add(category2)
db.session.commit()

now = datetime.now()
now_removed_hour_min = datetime(now.year, now.month, now.day)

task_title1 = 'Task 1'
task_description1 = 'Task 1 Description'
task_priority1 = Priority.LOW
task_deadline1 = now_removed_hour_min
task_time_length1 = TimeLength.FIFTEEN_MIN
task1 = Task(title=task_title1, description=task_description1, priority=task_priority1, deadline=task_deadline1, time_length=task_time_length1, user_id=user.id, category_id=category1.id)
task_title2 = 'Task 2'
task_description2 = 'Task 2 Description'
task_priority2 = Priority.HIGH
task_deadline2 = now_removed_hour_min + timedelta(days=1)
task_time_length2 = TimeLength.ONE_HOUR
task2 = Task(title=task_title2, description=task_description2, priority=task_priority2, deadline=task_deadline2, time_length=task_time_length2, user_id=user.id, category_id=category1.id)
task_title3 = 'Task 3'
task_description3 = 'Task 3 Description'
task_priority3 = Priority.AVERAGE
task_deadline3 = now_removed_hour_min + timedelta(days=7)
task_time_length3 = TimeLength.EIGHT_HOURS
task3 = Task(title=task_title3, description=task_description3, priority=task_priority3, deadline=task_deadline3, time_length=task_time_length3, user_id=user.id, category_id=category1.id)
task_title4 = 'Task 4'
task_description4 = 'Task 4 Description'
task_priority4 = Priority.LOW
task_deadline4 = now_removed_hour_min
task_time_length4 = TimeLength.FIFTEEN_MIN
task4 = Task(title=task_title4, description=task_description4, priority=task_priority4, deadline=task_deadline4, time_length=task_time_length4, user_id=user.id, category_id=category2.id)
task_title5 = 'Task 5'
task_description5 = 'Task 5 Description'
task_priority5 = Priority.HIGH
task_deadline5 = now_removed_hour_min + timedelta(days=1)
task_time_length5 = TimeLength.ONE_HOUR
task5 = Task(title=task_title5, description=task_description5, priority=task_priority5, deadline=task_deadline5, time_length=task_time_length5, user_id=user.id, category_id=category2.id)
task_title6 = 'Task 6'
task_description6 = 'Task 6 Description'
task_priority6 = Priority.AVERAGE
task_deadline6 = now_removed_hour_min + timedelta(days=7)
task_time_length6 = TimeLength.EIGHT_HOURS
task6 = Task(title=task_title6, description=task_description6, priority=task_priority6, deadline=task_deadline6, time_length=task_time_length6, user_id=user.id, category_id=category2.id)

# input user specific tasks
db.session.add(task1)
db.session.add(task2)
db.session.add(task3)
db.session.add(task4)
db.session.add(task5)
db.session.add(task6)
db.session.commit()