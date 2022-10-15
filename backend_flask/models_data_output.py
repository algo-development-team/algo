from models import User, Workspace, Category, Task

# get all users
users = User.query.all()
print('len(users): ' + str(len(users)))
for user in users:
  print(str(user.id) + ': ' + user.__repr__())
  print('checklist ' + str(user.id) + ': '  + str(user.checklist))
  print('work_days ' + str(user.id) + ': '  + str(user.work_days))
  print('calendar_id ' + str(user.id) + ': '  + str(user.calendar_id))

# get all workspaces
workspaces = Workspace.query.all()
print('len(workspaces): ' + str(len(workspaces)))
for workspace in workspaces:
  print(str(workspace.id) + ': ' + workspace.__repr__())
  print('members ' + str(workspace.id) + ': '  + str(workspace.members))
  print('admins ' + str(workspace.id) + ': '  + str(workspace.admins))

# get all categories
categories = Category.query.all()
print('len(categories): ' + str(len(categories)))
for category in categories:
  print(str(category.id) + ': ' + category.__repr__() + ' / workspace_id: ' + str(category.workspace_id))

# get all tasks
tasks = Task.query.all()
print('len(tasks): ' + str(len(tasks)))
for task in tasks:
  print(str(task.id) + ': ' + task.__repr__() + ' / category_id: ' + str(task.category_id) + ' / user_id: ' + str(task.user_id))