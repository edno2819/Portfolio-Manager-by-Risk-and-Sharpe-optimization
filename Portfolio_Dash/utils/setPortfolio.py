from scipy.optimize import minimize
import yfinance as yf
from utils.portfolio import *
from utils.utilitarios import *
import numpy  as np
from utils.graphPortfolio import GraphPort
from utils.variaveis import *
import pandas as pd
import pickle

def carregar_dados(name):
    with open(f'dados_assets/{name}.obj', 'rb') as inp:
        tech_companies = pickle.load(inp)
        return  tech_companies


def salvar(obj, name):
    save_object(obj, f'dados_assets/{name}.obj')


def setDataClose(assets, start, end, interval):
    dataset = yf.download(assets, start=start, end=end, interval=interval)
    names_to_drop = []
    #VERIFICANDO ATIVOS SEM VALORES
    num_nan = dataset['Adj Close'].isna().sum()
    for ativo in num_nan.keys():
        if num_nan[ativo]>min(num_nan):
            names_to_drop.append(ativo)
            print(f'Erro no ativo {ativo}')

    #DELETANDO LINHAS VAZIAS
    CLOSES = dataset['Adj Close'].drop(columns=names_to_drop)
    CLOSES = CLOSES.dropna()

    return dataset , CLOSES


def createSetPortfolio(assets, start, end, interval, atualization, dates_to_calculate):
    ports = []
    _ , CLOSES = setDataClose(assets, start, end, interval)

    
    for c in range(dates_to_calculate, len(list(CLOSES.index)), atualization):
        ports.append(Portifolio())
        port = ports[-1] 

        assets_name = list(CLOSES.columns)
        port.dates =  list(CLOSES.index)[c:c+atualization+1]

        for asset in assets_name:
            data =  np.array(list(CLOSES[asset].array))[c:c+atualization+1]
            data = data[np.logical_not(np.isnan(data))]
            if len(data)>0:
                dates = list(CLOSES[asset].dropna().index)[c:c+atualization+1]
                port.add_asset(asset, data)
                port.assets_dates[asset] = dates

    return ports


def createSetPortfolioToMinimize(assets, start, end, interval, atualization, dates_to_calculate):
    ports = []
    dataset , CLOSES = setDataClose(assets, start, end, interval)
    
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
    dataset , CLOSES = setDataClose(assets, start, end, interval)

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
    CLOSES = data['Adj Close']
    CLOSES = CLOSES.dropna()

    port.dates =  list(CLOSES.index)
    
    data =  np.array(list(CLOSES.array))
    data = data[np.logical_not(np.isnan(data))][dates_to_calculate:]
    if len(data)>0:
        port.add_asset(asset, data)
        port.assets_dates[asset] = list(CLOSES.index)[dates_to_calculate:]

    port.set_max_datas()


def set_assets_portfolio_carregados(port, asset, start, end, interval, dates_to_calculate):
    df = carregar_dados(asset+interval)
    CLOSES = df[(df.index >= start) & (df.index <= end)]

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



def createPortfolio(assets, interval, start, end, atualization, dates_to_calculate, tipo):
    ports_to_mini = createSetPortfolioToMinimize(assets, start, end, INTERVAL[interval], atualization, dates_to_calculate)

    if ports_to_mini==[]:
        return False, False, False, False, False
    
    ports = createSetPortfolio(assets, start, end, INTERVAL[interval], atualization, dates_to_calculate)

    if ports_to_mini[-1].assets_cov=={}:
        del ports_to_mini[-1]
        del ports[-1]

    ports_to_mini = setPortfolio(ports_to_mini, interval)
    vetor_pesos = minimize_ports(ports_to_mini, tipo)
    #vetor_pesos = []
    # for c in range(len(ports_to_mini)):
    #     vetor_pesos.append([round(1/len(ports_to_mini[0].port.keys()),4) for c in ports_to_mini[0].port.keys()])


    ports = setPortfolio(ports, interval)

    risco, retur, sharpe = calculateRiscoMedio(ports_to_mini, vetor_pesos)

    comps, comps_taxa = {}, {}

    #PORTFOLIO BRUTO
    port_2 = Portifolio()
    dataset = set_assets_portfolio(port_2, assets, start, end, INTERVAL[interval], dates_to_calculate)
    port_2.set_max_datas()
    comps['Portfolio Bruto'] = port_2
    comps_taxa['Portfolio Bruto TAXA'] = [round(1/len(vetor_pesos[0]),3) for c in vetor_pesos[0]]

    # #COMPARATIVO
    # port_sp500 = Portifolio()
    # set_assets_portfolio_carregados(port_sp500, ATIVOS['S&P 500'], start, end, INTERVAL[interval], dates_to_calculate)
    # port_sp500.set_max_datas() 
    # comps['S&P 500'] = port_sp500
    # comps_taxa['S&P 500 TAXA'] = [1]

    #COMPARATIVO2
    port_ibovespa = Portifolio()
    set_assets_portfolio_carregados(port_ibovespa, ATIVOS['IBOVESPA'], start, end, INTERVAL[interval], dates_to_calculate)
    port_ibovespa.set_max_datas() 
    comps['IBOVESPA'] = port_ibovespa
    comps_taxa['IBOVESPA TAXA'] = [1]

    #INSTANCIANDO A CLASSE DOS GRÁFICOS
    GrapPor = GraphPort(ports, vetor_pesos, comps, comps_taxa)
    GrapPor.ports_to_mini = ports_to_mini

    return GrapPor, risco, retur, sharpe, dataset
