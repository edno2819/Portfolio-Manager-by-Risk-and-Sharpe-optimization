from scipy.optimize import minimize
import matplotlib.pyplot as plt
import yfinance as yf
from portfolio import *
import numpy  as np
import seaborn as sns
import pandas as pd


COLORS = ['red','blue','skyblue','orange', 'green',]
sns.set_style('darkgrid', {'legend.frameon':True})
INTERVAL = {'5 Dias':'5d','1 Semana':'1wk','1 Mês':'1mo','3 Mêses':'3mo'}



def createSetPortfolio(assets, start, end, interval, atualization, dates_to_calculate):
    ports = []
    #data = yf.download(assets, start=start, end=end, interval=interval)
    #data.to_excel('assets_dados_semanal.xlsx')
    data = pd.read_excel('assets_dados_semanal.xlsx', header=[0, 1])
    CLOSES = data['Adj Close']
    CLOSES = CLOSES.dropna()
    
    for c in range(dates_to_calculate, len(list(CLOSES.index)), atualization):
        ports.append(Portifolio())
        port = ports[-1] 

        assets_name = list(CLOSES.columns)
        port.dates =  list(CLOSES.index)[c:c+atualization]

        for asset in assets_name:
            data =  np.array(list(CLOSES[asset].array))[c:c+atualization]
            data = data[np.logical_not(np.isnan(data))]
            if len(data)>0:
                dates = list(CLOSES[asset].dropna().index)[c:c+atualization]
                port.add_asset(asset, data)
                port.assets_dates[asset] = dates

    return ports

def createSetPortfolioToMinimize(assets, start, end, interval, atualization, dates_to_calculate):
    ports = []
    #data = yf.download(assets, start=start, end=end, interval=interval)
    #data.to_excel('assets_dados_semanal.xlsx')
    data = pd.read_excel('assets_dados_semanal.xlsx', header=[0, 1])
    CLOSES = data['Adj Close']
    CLOSES = CLOSES.dropna()
    
    for c in range(dates_to_calculate, len(list(CLOSES.index)), atualization):
        ports.append(Portifolio())
        port = ports[-1] 

        assets_name = list(CLOSES.columns)
        port.dates =  list(CLOSES.index)[c-dates_to_calculate:c]

        for asset in assets_name:
            data =  np.array(list(CLOSES[asset].array))[c-dates_to_calculate:c]
            data = data[np.logical_not(np.isnan(data))]
            if len(data)>0:
                dates = list(CLOSES[asset].dropna().index)[c-dates_to_calculate:c]
                port.add_asset(asset, data)
                port.assets_dates[asset] = dates

    return ports

def setPortfolio(ports):
    for port in ports:
        port.set_max_datas()
        port.set_to_calculate_risk()
        port.calculate_return()
    return ports

def minimize_portfolio(port):
    assets_name = list(port.port.keys())
    limites = tuple([(0, 1) for c in range(len(assets_name))])
    x0 = [1/len(assets_name) for c in range(len(assets_name))]
    cons = ({'type': 'eq', 'fun': lambda x:  np.sum(x) - 1})
    result = minimize(port.sharpe_ratio_invert, x0, method='SLSQP', bounds=limites, constraints=cons)
    return result.x

def minimize_ports(ports):
    vetor_pesos = []
    for port in ports:
        vetor_pesos.append(minimize_portfolio(port))
    return vetor_pesos



start = "2009-01-01"
end = "2015-04-30"
interval="1 Semana"
assets = "SPY AAPL VALE MSFT VALE ITUB UNH BAC CCL DVN MU"
atualization = 4
dates_to_calculate = 52
ports_to_mini = createSetPortfolioToMinimize(assets, start, end, INTERVAL[interval], atualization, dates_to_calculate)
ports_to_mini = setPortfolio(ports_to_mini)
vetor_pesos = minimize_ports(ports_to_mini)

ports = createSetPortfolio(assets, start, end, INTERVAL[interval], atualization, dates_to_calculate)

for port, pesos in zip(ports, vetor_pesos):
    port.chart_to_portfolio()
    port.circle_chart_portifolio(pesos)

