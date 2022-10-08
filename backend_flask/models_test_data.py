from models import User, Workspace, Category, Task, WorkspaceType, Priority, TimeLength
import datetime

user_name1 = 'YOUR_NAME_HERE'
user_email1 = 'YOUR_EMAIL_HERE'
user_refresh_token1 = 'YOUR_REFRESH_TOKEN_HERE'
user1 = User(name=user_name1, email=user_email1, refresh_token=user_refresh_token1)

workspace_name1 = 'Workspace 1'
workspace_workspace_type1 = WorkspaceType.WORK
workspace_members1 = [1]
workspace_admins1 = [1]
workspace1 = Workspace(name=workspace_name1, workspace_type=workspace_workspace_type1, members=workspace_members1, admins=workspace_admins1)

category_name1 = 'Category 1'
category1 = Category(name=category_name1, workspace_id=1)

task_title1 = 'Task 1'
task_description1 = 'Task 1 Description'
task_priority1 = Priority.HIGH
task_deadline = datetime.datetime(2022, 12, 31, 0, 0, 0)
task_time_length1 = TimeLength.EIGHT_HOURS
task1 = Task(title=task_title1, description=task_description1, priority=task_priority1, deadline=task_deadline, time_length=task_time_length1, category_id=1)