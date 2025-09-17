import requests
import os
import csv
from dotenv import load_dotenv
load_dotenv()

POLY_API_KEY = os.getenv('POLYGON_API_KEY')

LIMIT = 1000

url=f'https://api.polygon.io/v3/reference/tickers?market=stocks&active=true&order=asc&limit={LIMIT}&sort=ticker&apiKey={POLY_API_KEY}'

response = requests.get(url)
tickers=[]

data = response.json()

print(data['next_url'])
for ticker in data['results']:
    tickers.append(ticker)

while 'next_url' in data and len(tickers)<=3000:
    print('requesting next page', data['next_url'])
    response = requests.get(data['next_url'] + f'&apiKey={POLY_API_KEY}')
    data = response.json()
    print(data)
    for ticker in data['results']:
        tickers.append(ticker)
    print(len(tickers))

example_ticker = {'ticker': 'HUN', 'name': 'Huntsman Corporation', 'market': 'stocks', 'locale': 'us', 'primary_exchange': 'XNYS', 'type': 'CS', 'active': True, 'currency_name': 'usd', 'cik': '0001307954', 'composite_figi': 'BBG000NS26Q8', 'share_class_figi': 'BBG001SKWX22', 'last_updated_utc': '2025-09-16T06:05:51.697381664Z'}

fieldnames = list(example_ticker.keys())
output_csv = 'tickers.csv'
with open(output_csv, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for t in tickers:
        row = {key: t.get(key, '') for key in fieldnames}
        writer.writerow(row)
print(f'Wrote {len(tickers)} to {output_csv}')


