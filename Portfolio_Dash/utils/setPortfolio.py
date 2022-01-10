from scipy.optimize import minimize
import yfinance as yf
from utils.portfolio import *
import numpy  as np
from utils.graphPortfolio import GraphPort
from utils.variaveis import *


def set_assets_portfolio(port, assets, start, end, interval):
    data = yf.download(assets, start=start, end=end, interval=interval)
    CLOSES = data['Adj Close']
    port.dates =  list(CLOSES.dropna().index)
    assets_name = list(CLOSES.columns)
    


    for asset in assets_name:
        data =  np.array(list(CLOSES[asset].array))
        data = data[np.logical_not(np.isnan(data))]
        if len(data)>0:
            port.add_asset(asset, data)
            port.assets_dates[asset] = list(CLOSES[asset].dropna().index)

    port.set_max_datas()
    port.set_to_calculate_risk()
    port.calculate_return()


def set_assets_portfolio_unique(port, asset, start, end, interval):
    data = yf.download(asset, start=start, end=end, interval=interval)
    CLOSES = data['Adj Close']
    port.dates =  list(CLOSES.dropna().index)
    
    data =  np.array(list(CLOSES.array))
    data = data[np.logical_not(np.isnan(data))]
    if len(data)>0:
        port.add_asset(asset, data)
        port.assets_dates[asset] = list(CLOSES.dropna().index)

    port.set_max_datas()
    #port.set_to_calculate_risk()
    #port.calculate_return()


def minimize_portfolio(port):
    assets_name = list(port.port.keys())
    limites = tuple([(0, 1) for c in range(len(assets_name))])
    x0 = [1/len(assets_name) for c in range(len(assets_name))]

    cons = ({'type': 'eq', 'fun': lambda x:  np.sum(x) - 1})
    result = minimize(port.sharpe_ratio_invert, x0, method='SLSQP', bounds=limites, constraints=cons)

    if result.success:
        fitted_params = result.x
        risco = round(port.risk_portfolio(fitted_params),3)
        retorno = round(port.return_portfolio(fitted_params),3)
        sharpe_ratio = round(port.sharpe_ratio(fitted_params),3)
    else:
        raise ValueError(result.message)

    return {asse:round(taxa*100,2) for asse, taxa  in zip(assets_name,fitted_params)}, fitted_params, risco, retorno, sharpe_ratio


def createPortfolio(assets, interval, start, end):
    port = Portifolio()
    assets_name = set_assets_portfolio(port, assets, start, end, INTERVAL[interval])
    port.portifolio_set(interval)
    fitted_params, taxas_assets, risco, retorno, sharpe_ratio = minimize_portfolio(port)
    GrapPor = GraphPort(port, taxas_assets, fitted_params)

    end_new = "2021-05-30"
    interval_new = '1 Semana'
    port_2 = Portifolio()
    set_assets_portfolio(port_2, assets, end, end_new, INTERVAL[interval_new])
    port_2.portifolio_set(interval_new)

    #COMPARATIVO
    port_sp500 = Portifolio()
    set_assets_portfolio_unique(port_sp500, ATIVOS['S&P 500'], end, end_new, INTERVAL[interval_new])
    port_sp500.portifolio_set(interval_new)

    #COMPARATIVO2
    port_ibovespa = Portifolio()
    set_assets_portfolio_unique(port_ibovespa, ATIVOS['IBOVESPA'], end, end_new, INTERVAL[interval_new])
    port_ibovespa.portifolio_set(interval_new)

    comps = {'S&P 500':port_sp500, 'IBOVESPA':port_ibovespa, 'Portfolio Bruto':port_2}
    comps_taxa = {'S&P 500 TAXA':[1], 'IBOVESPA TAXA':[1], 'Portfolio Bruto TAXA':[round(1/len(taxas_assets),3) for c in taxas_assets]}

    GrapPor_extra = GraphPort(port_2, taxas_assets, fitted_params, comps, comps_taxa)

    return GrapPor, GrapPor_extra, risco, retorno, sharpe_ratio
