import yfinance as yf

#data = yf.download("SPY AAPL", start="2017-01-01", end="2017-04-30", interval='1m', period='ytd')
data = yf.download("SPY AAPL", start="2017-01-01", end="2017-04-30")
print(data)