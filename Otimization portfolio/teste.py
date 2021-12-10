import requests
# minha Key da API Alphavantage ZX467WMVV05FBUVQ
# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
# url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=demo'
# r = requests.get(url)
# data = r.json()

# print(data)

url = 'https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol=IBM&apikey=demo&horizon=3month'
r = requests.get(url)
data = r.json()

print(data)