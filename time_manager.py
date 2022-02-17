from datetime import datetime, date, timedelta
from dateutil import tz

def convert_to_local_time(str_date, str_exchange):

  from_zone = tz.tzutc()
  to_zone = tz.tzlocal()

  if str_exchange == 'Binance':
    utc = datetime.strptime(str_date, '%Y-%m-%d %H:%M:%S')
  elif str_exchange == 'Coinbase':
    utc = datetime.strptime(str_date, '%Y-%m-%dT%H:%M:%SZ')
  elif str_exchange == 'Coinbase Pro':
    utc = datetime.strptime(str_date, '%Y-%m-%dT%H:%M:%S.%fZ')

  utc = utc.replace(tzinfo = from_zone)
  local = utc.astimezone(to_zone)
  
  str_date = local.strftime('%Y-%m-%d')

  return str_date

def go_back_one_day(date_day):

  date_day -= timedelta(days = 1)

  return date_day

def convert_date_tax_purpose(str_date,bool_tax_purpose):

  date_day = date.fromisoformat(str_date)
  if bool_tax_purpose:
    date_day -= timedelta(days = 1)
  str_date = date_day.strftime('%Y-%m-%d')

  return date_day

def return_timestamp():
  
  return datetime.now().strftime("%Y%m%d_%H%M%S")