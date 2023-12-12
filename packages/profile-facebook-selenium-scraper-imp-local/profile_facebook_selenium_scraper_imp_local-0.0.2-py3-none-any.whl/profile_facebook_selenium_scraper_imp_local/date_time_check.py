import datetime as dt

date_now = dt.datetime.now()
str_temp = 2023
str_month = 12
str_day = 12
str_temp = dt.date(str_temp, str_month, str_day)
print(str_temp)
print(isinstance(str_temp, dt.date))
