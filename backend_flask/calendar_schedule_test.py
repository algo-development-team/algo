from calendar_schedule import add_task_time_blocks_to_calendar
from models import User
from datetime import timedelta

print('Enter the user\'s email address:')
email = input()
user = User.query.filter_by(email=email).first()

runtimes = add_task_time_blocks_to_calendar(user.id)
print('runtime_algorithm:')
print(timedelta(seconds=runtimes['runtime_algorithm']['seconds'], microseconds=runtimes['runtime_algorithm']['microseconds']))
print('runtime_calendar:')
print(timedelta(seconds=runtimes['runtime_calendar']['seconds'], microseconds=runtimes['runtime_calendar']['microseconds']))
print('runtime_total:')
print(timedelta(seconds=runtimes['runtime_total']['seconds'], microseconds=runtimes['runtime_total']['microseconds']))

# RUNTIME EFFICIENCY COMMENTS:

# COMMENT 1:
# after testing each type of request functions, all request functions have similar runtime
# thus, reducing the number of requests is the best way to improve the runtime
