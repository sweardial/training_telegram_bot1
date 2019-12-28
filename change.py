import requests
import json


def get_exchange_rate_usd():
    link = 'https://api.exchangeratesapi.io/latest?base=USD'
    r = requests.get(link).json()
    usd = r['rates']['RUB']
    return round(usd, 2)

def get_exchange_rate_eur():
    link = 'https://api.exchangeratesapi.io/latest?base=EUR'
    r = requests.get(link).json()
    eur = r['rates']['RUB']
    return round(eur, 2)

d = get_exchange_rate_usd()
b = get_exchange_rate_eur()
with open('exchange.json', 'w') as file:
    json.dump([b, d], file, indent=4, ensure_ascii=False)


