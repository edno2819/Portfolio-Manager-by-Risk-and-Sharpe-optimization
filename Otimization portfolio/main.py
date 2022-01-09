from scipy.optimize import minimize
import yfinance as yf
from portfolio import *
import numpy  as np

port = Portifolio()

def set_assets_portfolio():
    start = "2010-01-01"
    end = "2015-04-30"
    interval="3mo"
    assets = "SPY AAPL FB VALE MSFT VALE ITUB UNH BAC CCL DVN MU"


    data = yf.download(assets, start=start, end=end, interval=interval)
    CLOSES = data['Adj Close']
    dates_assets = list(CLOSES.dropna().index)
    assets_name = list(CLOSES.columns)


    for asset in assets_name:
        data =  np.array(list(CLOSES[asset].array))
        data = data[np.logical_not(np.isnan(data))]
        if len(data)>0:
            port.add_asset(asset, data)
            port.assets_dates[asset] = list(CLOSES[asset].dropna().index)
    
    port.dates = dates_assets

    port.set_to_calculate_risk()
    port.calculate_return()
    return assets_name

def minimize_portfolio():
    limites = tuple([(0, 1) for c in range(len(assets_name))])
    x0 = [1/len(assets_name) for c in range(len(assets_name))]

    cons = ({'type': 'eq', 'fun': lambda x:  np.sum(x) - 1})
    result = minimize(port.sharpe_ratio_invert, x0, method='SLSQP', bounds=limites, constraints=cons)

    if result.success:
        fitted_params = result.x
        print('\n')
        for asset in range(len(assets_name)):
            print(f"Ação {assets_name[asset]} {round(fitted_params[asset]*100,2)}%")
        print('\n')
        print(f'Risco do portifólio: {round(port.risk_portfolio(fitted_params),3)}%')
        print(f'Retorno do portifólio: {round(port.return_portfolio(fitted_params, tipo=True),3)}%')
        print(f'Indici Sharpe do portifólio: {round(port.sharpe_ratio(fitted_params, risk_free_rate=0.006),3)}')
        print('\n')
    else:
        raise ValueError(result.message)


start = "2010-01-01"
end = "2015-04-30"
interval="3mo"
assets = "SPY AAPL FB VALE MSFT VALE ITUB UNH BAC CCL DVN MU"


data = yf.download(assets, start=start, end=end, interval=interval)
CLOSES = data['Adj Close']
dates_assets = list(CLOSES.dropna().index)
assets_name = list(CLOSES.columns)


for asset in assets_name:
    data =  np.array(list(CLOSES[asset].array))
    data = data[np.logical_not(np.isnan(data))]
    if len(data)>0:
        port.add_asset(asset, data)
        port.assets_dates[asset] = list(CLOSES[asset].dropna().index)

port.dates = dates_assets

port.set_to_calculate_risk()
port.calculate_return()

limites = tuple([(0, 1) for c in range(len(assets_name))])
x0 = [1/len(assets_name) for c in range(len(assets_name))]

cons = ({'type': 'eq', 'fun': lambda x:  np.sum(x) - 1})
result = minimize(port.sharpe_ratio_invert, x0, method='SLSQP', bounds=limites, constraints=cons)

if result.success:
    fitted_params = result.x
    print('\n')
    for asset in range(len(assets_name)):
        print(f"Ação {assets_name[asset]} {round(fitted_params[asset]*100,2)}%")
    print('\n')
    print(f'Risco do portifólio: {round(port.risk_portfolio(fitted_params),3)}%')
    print(f'Retorno do portifólio: {round(port.return_portfolio(fitted_params),3)}%')
    print(f'Indici Sharpe do portifólio: {round(port.sharpe_ratio(fitted_params, risk_free_rate=0.006),3)}')
    print('\n')
else:
    raise ValueError(result.message)

a = port.return_portfolio(fitted_params)
hg = port.chart_to_portfolio_return_porcent(fitted_params)
jk = port.chart_to_portfolio()
