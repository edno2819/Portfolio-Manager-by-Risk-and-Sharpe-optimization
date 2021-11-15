from scipy.optimize import minimize, rosen
import yfinance as yf
from portfolio import *
import numpy  as np


assets = "SPY AAPL TSLA FB"
start = "2016-01-01"
end = "2021-04-30"
interval="3mo"

data = yf.download(assets, start=start, end=end, interval=interval)
CLOSES = data['Adj Close']
assets_name = list(CLOSES.columns)

a = portifolio()

def equal_minimun(propor:list):
    taxas = {assets_name[asset]:propor[asset] for asset in range(len(assets_name))}
    return a.risk_portfolio(taxas)

for asset in assets_name:
    data =  np.array(list(CLOSES[asset].array))
    data = data[np.logical_not(np.isnan(data))]
    a.add_asset(asset, data)

a.set_to_calculate_risk()
a.calculate_return()


restricoes = ({'type': 'ineq', 'fun': lambda x:  x[0] - 2 * x[1] + 2},
        {'type': 'ineq', 'fun': lambda x: -x[0] - 2 * x[1] + 6},
        {'type': 'ineq', 'fun': lambda x: -x[0] + 2 * x[1] + 2})

limites = tuple([(0, 1) for c in range(len(assets_name))])
x0 = [1/len(assets_name) for c in range(len(assets_name))]


result = minimize(equal_minimun, x0, method='SLSQP', bounds=limites)#, constraints=restricoes)
if result.success:
    fitted_params = result.x
    print(fitted_params)
else:
    raise ValueError(result.message)



