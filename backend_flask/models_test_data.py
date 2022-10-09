from models import User, Workspace, Category, Task, WorkspaceType, Priority, TimeLength
import datetime

user_name1 = 'YOUR_NAME_HERE1'
user_email1 = 'YOUR_EMAIL_HERE1'
user_picture1 = 'YOUR_USER_PICTURE_HERE1'
user_refresh_token1 = 'YOUR_REFRESH_TOKEN_HERE1'
user1 = User(name=user_name1, email=user_email1, picture=user_picture1, refresh_token=user_refresh_token1)
user_name2 = 'YOUR_NAME_HERE2'
user_email2 = 'YOUR_EMAIL_HERE2'
user_picture2 = 'YOUR_USER_PICTURE_HERE2'
user_refresh_token2 = 'YOUR_REFRESH_TOKEN_HERE2'
user2 = User(name=user_name2, email=user_email2, picture=user_picture2, refresh_token=user_refresh_token2)
user_name3 = 'YOUR_NAME_HERE3'
user_email3 = 'YOUR_EMAIL_HERE3'
user_picture3 = 'YOUR_USER_PICTURE_HERE3'
user_refresh_token3 = 'YOUR_REFRESH_TOKEN_HERE3'
user3 = User(name=user_name3, email=user_email3, picture=user_picture3, refresh_token=user_refresh_token3)

workspace_name1 = 'Workspace 1'
workspace_workspace_type1 = WorkspaceType.WORK
workspace_members1 = [1, 2, 3]
workspace_admins1 = [1, 2]
workspace1 = Workspace(name=workspace_name1, workspace_type=workspace_workspace_type1, members=workspace_members1, admins=workspace_admins1)
workspace_name2 = 'Workspace 2'
workspace_workspace_type2 = WorkspaceType.WORK
workspace_members2 = [1, 2]
workspace_admins2 = [1]
workspace2 = Workspace(name=workspace_name2, workspace_type=workspace_workspace_type2, members=workspace_members2, admins=workspace_admins2)
workspace_name3 = 'Workspace 3'
workspace_workspace_type3 = WorkspaceType.WORK
workspace_members3 = [3]
workspace_admins3 = [3]
workspace3 = Workspace(name=workspace_name3, workspace_type=workspace_workspace_type3, members=workspace_members3, admins=workspace_admins3)

category_name1 = 'Category 1'
category1 = Category(name=category_name1, workspace_id=1)
category_name2 = 'Category 2'
category2 = Category(name=category_name2, workspace_id=1)
category_name3 = 'Category 3'
category3 = Category(name=category_name3, workspace_id=2)

task_title1 = 'Task 1'
task_description1 = 'Task 1 Description'
task_priority1 = Priority.LOW
task_deadline1 = datetime.datetime(2022, 12, 31, 0, 0, 0)
task_time_length1 = TimeLength.FIFTEEN_MIN
task1 = Task(title=task_title1, description=task_description1, priority=task_priority1, deadline=task_deadline1, time_length=task_time_length1, user_id=1, category_id=1)
task_title2 = 'Task 2'
task_description2 = 'Task 2 Description'
task_priority2 = Priority.LOW
task_deadline2 = datetime.datetime(2022, 12, 31, 0, 0, 0)
task_time_length2 = TimeLength.FIFTEEN_MIN
task2 = Task(title=task_title2, description=task_description2, priority=task_priority2, deadline=task_deadline2, time_length=task_time_length2, user_id=1, category_id=1)
task_title3 = 'Task 3'
task_description3 = 'Task 3 Description'
task_priority3 = Priority.LOW
task_deadline3 = datetime.datetime(2022, 12, 31, 0, 0, 0)
task_time_length3 = TimeLength.FIFTEEN_MIN
task3 = Task(title=task_title3, description=task_description3, priority=task_priority3, deadline=task_deadline3, time_length=task_time_length3, user_id=1, category_id=2)