from datetime import datetime, date, timedelta
from dateutil import tz
from requests import get

def convert_to_local_time(str_date, str_exchange):

  from_zone = tz.tzutc()
  to_zone = tz.tzlocal()

  if str_exchange == 'Binance' or str_exchange == 'Revolut':
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

def check_status(str_code, date_day):

  str_url = f'http://api.nbp.pl/api/exchangerates/rates/a/{str_code}/{date_day}/'
  req_resp = get(str_url)

  return req_resp

def nbp_exchange_rates(str_date,str_code, bool_tax_purpose):

  f_exchange_rate = 0.0
  date_day = convert_date_tax_purpose(str_date,bool_tax_purpose)
  if str_code == 'PLN':
    return 1.0, date_day
  req_status = check_status(str_code,date_day).status_code
  while req_status != 200:
    date_day = go_back_one_day(date_day)
    req_status = check_status(str_code,date_day).status_code
  try:
    req_data = check_status(str_code,date_day).json()
    f_exchange_rate = float(req_data['rates'][0]['mid'])
  except:
    return f_exchange_rate, date_day

  return f_exchange_rate, date_day