#@title  Sprawdź historyczny kurs waluty  {"run": "auto"}

from requests import get
from datetime import date, timedelta

code = "EUR" #@param ["USD", "EUR", "CHF", "GBP"]
day = "2021-12-12" #@param {type:"date"}
day = date.fromisoformat(day)

url = f'http://api.nbp.pl/api/exchangerates/rates/a/{code}/{day}/'

resp = get(url)
print(resp)
if resp.status_code != 404:
  data = resp.json()
  #print(data)

  exchange_rate = data['rates'][0]['mid']
  print(f'1 {code} = {exchange_rate} PLN w dniu {day}')
else:
  print('Weekend')
  workday = day
  url = f'http://api.nbp.pl/api/exchangerates/rates/a/{code}/{workday}/'
  resp = get(url)
  while resp.status_code == 404:
    workday = workday - timedelta(days = 1)
    print(workday)
    url = f'http://api.nbp.pl/api/exchangerates/rates/a/{code}/{workday}/'
    resp = get(url)
  data = resp.json()
  exchange_rate = data['rates'][0]['mid']
  print(f'1 {code} = {exchange_rate} PLN w dniu {workday}')