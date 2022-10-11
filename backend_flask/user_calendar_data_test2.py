from datetime import datetime
from user_calendar_data import parse_user_time_range, get_period_ranges
from pprint import pprint

def sep():
  print('----------------------------------------------------------------')

start_time = datetime(2022, 10, 10, 0, 0)
end_time = datetime(2022, 10, 11, 0, 0)
time_range = (start_time, end_time)
work_time_range = '9:00-17:00'
sleep_time_range = '23:00-7:00'

parsed_work_time_range = parse_user_time_range(work_time_range)
parsed_sleep_time_range = parse_user_time_range(sleep_time_range)

period_ranges = get_period_ranges(time_range, parsed_work_time_range, parsed_sleep_time_range)

sep()
print('Tested Functions:')
print('parse_user_time_range')
print('get_period_ranges')
sep()
sep()
print('Parsed User Time Ranges:')
pprint(parsed_work_time_range)
pprint(parsed_sleep_time_range)
sep()
sep()
print('Period Ranges:')
pprint(period_ranges)
sep()
