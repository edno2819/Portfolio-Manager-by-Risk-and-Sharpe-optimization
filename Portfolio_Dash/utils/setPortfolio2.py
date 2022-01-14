from scipy.optimize import minimize
import yfinance as yf
from utils.portfolio import *
import numpy  as np
from utils.graphPortfolio2 import GraphPort
from utils.variaveis import *
import pandas as pd



def createSetPortfolio(assets, start, end, interval, atualization, dates_to_calculate):
    ports = []
    data = yf.download(assets, start=start, end=end, interval=interval)
    #data.to_excel('assets_dados_semanal.xlsx')
    #data = pd.read_excel('assets_dados_semanal.xlsx', header=[0, 1])
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
    data = yf.download(assets, start=start, end=end, interval=interval)
    #data.to_excel('assets_dados_semanal.xlsx')
    #data = pd.read_excel('assets_dados_semanal.xlsx', header=[0, 1])
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


def set_assets_portfolio(port, assets, start, end, interval, dates_to_calculate):
    data = yf.download(assets, start=start, end=end, interval=interval)
    dataset = data.dropna()
    #data = pd.read_excel('assets_dados_semanal.xlsx', header=[0, 1])
    CLOSES = data['Adj Close']
    port.dates =  list(CLOSES.dropna().index)
    assets_name = list(CLOSES.columns)
    


    for asset in assets_name:
        data =  np.array(list(CLOSES[asset].array))
        data = data[np.logical_not(np.isnan(data))][dates_to_calculate:]
        if len(data)>0:
            port.add_asset(asset, data)
            port.assets_dates[asset] = list(CLOSES[asset].dropna().index)[dates_to_calculate:]

    port.set_max_datas()
    port.set_to_calculate_risk()
    port.calculate_return()
    return dataset


def set_assets_portfolio_unique(port, asset, start, end, interval, dates_to_calculate):
    data = yf.download(asset, start=start, end=end, interval=interval)
    #data = pd.read_excel('assets_dados_semanal.xlsx', header=[0, 1])
    CLOSES = data['Adj Close']
    CLOSES = CLOSES.dropna()
    port.dates =  list(CLOSES.index)
    
    data =  np.array(list(CLOSES.array))
    data = data[np.logical_not(np.isnan(data))][dates_to_calculate:]
    if len(data)>0:
        port.add_asset(asset, data)
        port.assets_dates[asset] = list(CLOSES.index)[dates_to_calculate:]

    port.set_max_datas()



def setPortfolio(ports, interval):
    for port in ports:
        port.set_max_datas()
        try:
            port.set_to_calculate_risk()
        except:
            tes = 1
            port.set_to_calculate_risk()
        port.calculate_return()
        port.set_max_datas()
        port.interval = interval

    return ports


def minimize_portfolio(port, function):
    assets_name = list(port.port.keys())
    limites = tuple([(0, 1) for c in range(len(assets_name))])
    x0 = [1/len(assets_name) for c in range(len(assets_name))]
    cons = ({'type': 'eq', 'fun': lambda x:  np.sum(x) - 1})

    result = minimize(function, x0, method='SLSQP', bounds=limites, constraints=cons)


    return result.x


def minimize_ports(ports, tipo):
    vetor_pesos = []
    for port in ports:

        if tipo=='sharpe':
            function = port.sharpe_ratio_invert
        elif tipo=='retorno':
            function = port.return_portfolio_invert
        elif tipo=='risco':
            function = port.risk_portfolio

        vetor_pesos.append(minimize_portfolio(port, function))
    return vetor_pesos


def calculateRiscoMedio(ports, pesos):
    risco, returno, sharpe = 0, 0, 0
    n = len(pesos)
    for port, peso in zip(ports, pesos):
        if type(port.risk_portfolio(peso))!=float:
            risco = 1
        risco += port.risk_portfolio(peso)
        returno += port.return_portfolio(peso)
        sharpe += port.sharpe_ratio(peso)

    return round(risco/n,3), round(returno/n,3), round(sharpe/n,3) 



def createPortfolio(assets, interval, start, end, atualization, dates_to_calculate, tipo='sharpe'):
    ports_to_mini = createSetPortfolioToMinimize(assets, start, end, INTERVAL[interval], atualization, dates_to_calculate)

    if ports_to_mini==[]:
        return False, False, False, False

    ports_to_mini = setPortfolio(ports_to_mini, interval)
    vetor_pesos = minimize_ports(ports_to_mini, tipo)
    ports = createSetPortfolio(assets, start, end, INTERVAL[interval], atualization, dates_to_calculate)
    ports = setPortfolio(ports, interval)

    risco, retur, sharpe = calculateRiscoMedio(ports, vetor_pesos)

    #PORTFOLIO BRUTO
    port_2 = Portifolio()
    dataset = set_assets_portfolio(port_2, assets, start, end, INTERVAL[interval], dates_to_calculate)
    port_2.set_max_datas() 

    #COMPARATIVO
    port_sp500 = Portifolio()
    set_assets_portfolio_unique(port_sp500, ATIVOS['S&P 500'], start, end, INTERVAL[interval], dates_to_calculate)
    port_sp500.set_max_datas() 

    #COMPARATIVO2
    port_ibovespa = Portifolio()
    set_assets_portfolio_unique(port_ibovespa, ATIVOS['IBOVESPA'], start, end, INTERVAL[interval], dates_to_calculate)
    port_ibovespa.set_max_datas() 

    comps = {'S&P 500':port_sp500, 'IBOVESPA':port_ibovespa, 'Portfolio Bruto':port_2}
    comps_taxa = {'S&P 500 TAXA':[1], 'IBOVESPA TAXA':[1], 'Portfolio Bruto TAXA':[round(1/len(vetor_pesos[0]),3) for c in vetor_pesos[0]]}

    GrapPor = GraphPort(ports, vetor_pesos, comps, comps_taxa)

    return GrapPor, risco, retur, sharpe, dataset
    #return GrapPor, 0.05, 0.05, 0.05, dataset
