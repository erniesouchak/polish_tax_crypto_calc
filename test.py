import requests
 
value, currency_code = input("Podaj kwotę do przeliczenia. Np 12.5 CHF\n").split()
url_template = f"http://api.nbp.pl/api/exchangerates/rates/a/{currency_code}"
rate = requests.get(url_template).json()["rates"][0]["mid"]
print(f"{value} {currency_code} = {rate * float(value)} PLN")