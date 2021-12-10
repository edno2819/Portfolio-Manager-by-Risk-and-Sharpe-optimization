from pandas.core.frame import DataFrame
import yfinance as yf
import pandas as pd


start = "2010-01-01"
end = "2019-12-30"
interval="1d"
assets = "SPY AAPL FB VALE MSFT"

for asset in assets.split(' '):
    dataset = yf.download(asset, start=start, end=end, interval=interval)
    dataset.drop(columns=['Adj Close'], inplace=True)
    dataset.dropna(inplace=True)
    dataset.to_csv(f'history_datas/{asset}_{interval}.csv', sep='\t')