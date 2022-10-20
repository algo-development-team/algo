from datetime import datetime

################################################################

# TEST

# use dts for testing get_dt_fifteen_min_rounded
dt1 = datetime(2022, 10, 9, 0, 18)
dt2 = datetime(2022, 10, 9, 0, 42)
dt3 = datetime(2022, 10, 9, 0, 27)
dt4 = datetime(2022, 10, 9, 0, 33)
dts = [(dt1, dt2), (dt3, dt4)]

# test string time comparison
str_ts = ['2022-10-10T08:45:00-04:00',
          '2022-10-10T16:30:00-04:00',
          '2022-10-11T13:00:00-04:00',
          '2022-10-11T14:30:00-04:00',
          '2022-10-12T10:30:00-04:00',
          '2022-10-12T14:30:00-04:00',
          '2022-10-12T16:30:00-04:00',
          '2022-10-11T12:00:00-04:00']

################################################################
