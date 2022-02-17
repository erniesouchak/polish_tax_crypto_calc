
from requests import get

import time_manager

def check_status(str_code, date_day):

  str_url = f'http://api.nbp.pl/api/exchangerates/rates/a/{str_code}/{date_day}/'
  req_resp = get(str_url)

  return req_resp

def nbp_exchange_rates(str_date,str_code, bool_tax_purpose):

  f_exchange_rate = 0.0
  date_day = time_manager.convert_date_tax_purpose(str_date,bool_tax_purpose)
  req_status = check_status(str_code,date_day).status_code
  while req_status != 200:
    date_day = time_manager.go_back_one_day(date_day)
    req_status = check_status(str_code,date_day).status_code
  try:
    req_data = check_status(str_code,date_day).json()
    f_exchange_rate = float(req_data['rates'][0]['mid'])
  except:
    return f_exchange_rate, date_day

  return f_exchange_rate, date_day